#!/usr/bin/env python3
"""Live job board scan: comparable openings, pay ranges, and competing demand for a role.

Pulls every job from a list of Ashby, Greenhouse, and Lever boards and keeps titles that
match --title. Pay ranges come straight from the postings, so they are verified figures.

Usage:
  python3 job_board_scan.py --title "product designer|design lead" [--location "new york|remote"]
  python3 job_board_scan.py --title "ml scientist|research scientist" --boards my_boards.txt

Board list format (one per line):  ashby:openai   greenhouse:anthropic   lever:netflix
Default list: boards.txt next to this script. Add boards there as new companies matter.
Output: markdown table, most recent first. Boards that fail to load are listed at the end.
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))


def get(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except Exception:
        return None


def scan(board, title_re, loc_re):
    kind, slug = board.split(":", 1)
    rows = []
    if kind == "ashby":
        d = get(f"https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true")
        if d is None:
            return board, None
        for j in d.get("jobs", []):
            loc = j.get("location") or ""
            if title_re.search(j["title"]) and (not loc_re or loc_re.search(loc)):
                comp = (j.get("compensation") or {}).get("compensationTierSummary")
                rows.append((slug, j["title"], loc, comp, (j.get("publishedAt") or "")[:10], j.get("jobUrl")))
    elif kind == "greenhouse":
        d = get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs")
        if d is None:
            return board, None
        for j in d.get("jobs", []):
            loc = (j.get("location") or {}).get("name") or ""
            if title_re.search(j["title"]) and (not loc_re or loc_re.search(loc)):
                det = get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs/{j['id']}?pay_transparency=true") or {}
                comp = None
                for p in det.get("pay_input_ranges") or []:
                    comp = f"${p['min_cents'] / 100:,.0f} to ${p['max_cents'] / 100:,.0f}"
                date = (det.get("first_published") or j.get("updated_at") or "")[:10]
                rows.append((slug, j["title"], loc, comp, date, j.get("absolute_url")))
    elif kind == "lever":
        d = get(f"https://api.lever.co/v0/postings/{slug}?mode=json")
        if d is None:
            return board, None
        for j in d:
            loc = (j.get("categories") or {}).get("location") or ""
            if title_re.search(j.get("text", "")) and (not loc_re or loc_re.search(loc)):
                sr = j.get("salaryRange") or {}
                comp = f"${sr['min']:,} to ${sr['max']:,}" if sr.get("min") else None
                rows.append((slug, j["text"], loc, comp, "", j.get("hostedUrl")))
    return board, rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", required=True, help="regex matched against job titles (case-insensitive)")
    ap.add_argument("--location", help="regex matched against job location (case-insensitive)")
    ap.add_argument("--boards", default=os.path.join(HERE, "boards.txt"))
    a = ap.parse_args()
    title_re = re.compile(a.title, re.I)
    loc_re = re.compile(a.location, re.I) if a.location else None
    boards = [l.strip() for l in open(a.boards) if l.strip() and not l.startswith("#")]
    with ThreadPoolExecutor(12) as ex:
        results = list(ex.map(lambda b: scan(b, title_re, loc_re), boards))
    failed = [b for b, r in results if r is None]
    rows = sorted((row for _, r in results if r for row in r), key=lambda x: x[4], reverse=True)
    print(f"Scanned {len(boards) - len(failed)} of {len(boards)} boards. {len(rows)} matching openings.\n")
    print("| Company | Title | Location | Pay range | Published | Link |")
    print("|---|---|---|---|---|---|")
    for c, t, l, comp, d, u in rows:
        cells = [c, t, l, comp or "not posted", d or "n/a", u]
        print("| " + " | ".join(str(x).replace("|", "/") for x in cells) + " |")
    if failed:
        print(f"\nBoards that did not load (slug may be wrong or board moved): {', '.join(failed)}", file=sys.stderr)


if __name__ == "__main__":
    main()
