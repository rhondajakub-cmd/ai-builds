#!/usr/bin/env python3
"""Rec intake: turn a job posting link into the fields the Talent Intelligence Agent needs.

Usage:
  python3 rec_intake.py <job-url>

Supports Ashby, Greenhouse, and Lever links through their public posting APIs.
Prints JSON: company, title, location, comp, employment_type, published, url, description.
Any other link exits with code 2 and a message; paste the job description instead.
"""
import html
import json
import re
import sys
import urllib.parse
import urllib.request


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def strip_html(s):
    s = re.sub(r"<(br|/p|/li|/h\d)[^>]*>", "\n", s or "", flags=re.I)
    s = re.sub(r"<li[^>]*>", "\n- ", s, flags=re.I)
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    return re.sub(r"\n\s*\n+", "\n\n", s).strip()


def ashby(org, job_id, url):
    d = get(f"https://api.ashbyhq.com/posting-api/job-board/{org}?includeCompensation=true")
    for j in d.get("jobs", []):
        if j.get("id") == job_id or job_id in (j.get("jobUrl") or ""):
            return {
                "company": org,
                "title": j.get("title"),
                "location": j.get("location"),
                "comp": (j.get("compensation") or {}).get("compensationTierSummary"),
                "employment_type": j.get("employmentType"),
                "published": (j.get("publishedAt") or "")[:10],
                "url": j.get("jobUrl") or url,
                "description": j.get("descriptionPlain") or strip_html(j.get("descriptionHtml")),
            }
    raise SystemExit(f"Ashby job {job_id} not found on the {org} board (it may be closed).")


def greenhouse(org, job_id, url):
    j = get(f"https://boards-api.greenhouse.io/v1/boards/{org}/jobs/{job_id}?pay_transparency=true")
    comp = None
    for p in j.get("pay_input_ranges") or []:
        lo, hi = p.get("min_cents", 0) / 100, p.get("max_cents", 0) / 100
        comp = f"${lo:,.0f} to ${hi:,.0f} {p.get('currency_type', '')}".strip()
    return {
        "company": org,
        "title": j.get("title"),
        "location": (j.get("location") or {}).get("name"),
        "comp": comp,
        "employment_type": None,
        "published": (j.get("first_published") or j.get("updated_at") or "")[:10],
        "url": j.get("absolute_url") or url,
        "description": strip_html(html.unescape(j.get("content") or "")),
    }


def lever(org, job_id, url):
    j = get(f"https://api.lever.co/v0/postings/{org}/{job_id}")
    sr = j.get("salaryRange") or {}
    comp = f"${sr['min']:,} to ${sr['max']:,} {sr.get('currency', '')}".strip() if sr.get("min") else None
    body = strip_html(j.get("description") or "") + "\n\n" + "\n\n".join(
        f"{l.get('text')}\n{strip_html(l.get('content'))}" for l in j.get("lists") or []
    )
    return {
        "company": org,
        "title": j.get("text"),
        "location": (j.get("categories") or {}).get("location"),
        "comp": comp,
        "employment_type": (j.get("categories") or {}).get("commitment"),
        "published": None,
        "url": j.get("hostedUrl") or url,
        "description": body.strip(),
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    url = sys.argv[1].strip()
    u = urllib.parse.urlparse(url)
    parts = [p for p in u.path.split("/") if p]
    q = urllib.parse.parse_qs(u.query)
    if u.netloc.endswith("ashbyhq.com") and len(parts) >= 2:
        out = ashby(parts[0], parts[1], url)
    elif "greenhouse.io" in u.netloc and "jobs" in parts:
        i = parts.index("jobs")
        out = greenhouse(parts[i - 1], parts[i + 1], url)
    elif u.netloc.endswith("lever.co") and len(parts) >= 2:
        out = lever(parts[0], parts[1], url)
    elif "gh_jid" in q:
        print(f"Greenhouse job id {q['gh_jid'][0]} on a company careers page. Find the board slug "
              "(boards.greenhouse.io/<slug>) and rerun with that link, or paste the job description.",
              file=sys.stderr)
        sys.exit(2)
    else:
        print("Not an Ashby, Greenhouse, or Lever link. Paste the job description instead.", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
