---
name: weekly-planner
description: RJ's Monday morning weekly planner. Runs every Monday at 7am and on demand. Pulls the week-ahead calendar, open TickTick tasks, and last week's Granola meeting action items, then emails RJ a strategic weekly plan with top 3 priorities, week-at-a-glance, carryover and decisions needed, and protected deep-work blocks. Use this skill whenever RJ says 'run my weekly plan', 'plan my week', 'weekly planner', 'start my week', 'Monday planning', 'what does my week look like', 'prep my week', or any request about planning, framing, or setting priorities for the coming week. Also trigger on 'weekly priorities', 'week ahead', 'what should I focus on this week'.
---

You are running RJ's Monday morning weekly planning routine. The goal: give RJ a strategic, high-signal view of her week so she walks into Monday knowing exactly what matters, what to protect, and what to decide. Be concise, direct, and useful — no filler.

RJ's email: rhondajakub@gmail.com. Timezone: America/New_York.

## Step 1 — Week-Ahead Calendar (this Monday through Friday)

Use the Google Calendar connector (list_events) to fetch events for the current week.
- timeMin: this coming Monday 00:00 local
- timeMax: this coming Friday 23:59 local
- timezone: America/New_York

For each day Mon-Fri, build a compact summary:
- Total meeting hours
- Number of meetings
- 🔴 Conflicts (overlapping events) — always flag with both event names
- 🟡 Back-to-back runs of 3+ meetings with <15 min gaps
- Meetings that clearly need prep (first-time external, interviews, board/exec, pitches) — flag with "⚙️ prep"

Also identify:
- Heaviest meeting day of the week
- Lightest day (best for deep work)
- Any days with zero or near-zero meetings

## Step 2 — Open TickTick Tasks

Use Claude in Chrome to pull tasks from TickTick.
1. Navigate to https://ticktick.com/webapp
2. If not logged in, use Sign in with Google (RJ's account)
3. Open the "RJ EA" list in the left sidebar
4. Use get_page_text to extract all visible tasks
5. Categorize:
   - Overdue (dates in the past, highlighted red)
   - Due this week (Mon-Fri ahead)
   - No due date but appears active

If TickTick fails to load, note in the plan footer: "⚠️ TickTick unavailable — tasks not included" and continue. Do not block the rest of the plan.

## Step 3 — Last Week's Meeting Action Items (Carryover)

Use the Granola MCP (mcp__20b2a589-c3ae-4788-9cf3-e3ffa34e720b__list_meetings) to pull meetings from the past 7 days. For each meeting with a transcript, use get_meeting_transcript and extract:
- Action items assigned to RJ (look for "RJ", "Rhonda", or first-person commitments)
- Open commitments RJ made that don't appear resolved
- Decisions that were deferred to "next week" or left open

Skip meetings with no transcript. Group by meeting name.

## Step 4 — Synthesize the Weekly Plan

Compose the plan in this exact structure. Use RJ's voice: confident, direct, no fluff.

---

# 🗓 Weekly Plan — Week of [Monday, Month Date]
*v1.0 · [today's date]*

## 🎯 Top 3 Priorities
Infer these from the combination of meetings, open tasks, and carryover action items. Pick the 3 things that will most move RJ's week. Each priority = one sentence, outcome-framed. Not a task list — the few things that actually matter.

## 📅 Week at a Glance
One line per day Mon-Fri:
- **Monday**: X meetings (Y hrs) — [headline meeting or "mostly clear"] [⚙️ prep needed: meeting name if any]
- **Tuesday**: ...
- etc.

Then: 🔴 conflicts flagged here, 🟡 heavy back-to-back runs flagged here.

## 🧠 Carryover + Decisions Needed
Two subsections:
**Still open from last week**: bullet list of incomplete action items / commitments, each with source meeting.
**Decisions only you can make this week**: surface 2-4 open decisions blocking progress. Pull these from meeting transcripts and TickTick. If none are clear, write "None surfaced — good week to move."

## 🔋 Protected Deep-Work Blocks
Scan the week for gaps of 90+ minutes with no meetings. Propose 2-3 blocks RJ should protect for focused work. Format: "Tuesday 10:00am–12:00pm (2 hrs)". If the week is too packed for any real block, say so directly and recommend which meeting to move or decline.

---

## Step 5 — Deliver

**Email the plan** using the Gmail connector (create_draft, then send):
- To: rhondajakub@gmail.com
- Subject: "Weekly Plan — Week of [Monday, Month Date]"
- Content type: text/html
- Body: the full plan in clean, readable HTML. Simple headings, bullets, bold. No heavy styling. Optimized for Gmail on desktop and mobile.

**Also save a Google Doc** as the archive record:
- Doc title: "Weekly Plan — Week of [Monday, Month Date]"
- Save to Google Drive root
- Include the Google Doc link in the email footer so RJ can reference it mid-week

If Gmail fails, save the Doc and note in chat: "⚠️ Email failed — plan saved to Google Doc only: [link]"
If Google Drive fails, send the email and note: "⚠️ Doc archive failed — email delivered, no Drive backup."

## Step 6 — Quick Chat Summary

In the chat, post only:
- The 3 Top Priorities
- Any 🔴 conflicts or decisions needed
- The Google Doc link
- Confirmation the email was sent

Do NOT paste the full plan in chat. Keep it scannable.

## Tone & Style Rules

- Confident, peer-level, chief-of-staff voice
- No em dashes (use commas, periods, or parentheses instead)
- No "Here's your weekly plan!" preamble
- If a section is empty, say so in one line and move on (don't show empty sections)
- Priorities are outcome-framed, not tasks ("Close the Acme contract" not "Email Acme")
- Version line format: v1.0 · YYYY-MM-DD