---
name: ss
description: RJ's visual shorthand. Grabs the most recent screenshot(s) from her Desktop and acts on them based on her instruction. Use whenever RJ types "/ss" with optional count and instruction (e.g. "/ss huh", "/ss 3 make infographic plz", "/ss fix", "/ss do this"). The skill lists screenshots newest→oldest, picks the top N (default 1), reads them, and performs the requested action.
---

# /ss — Screenshot Shorthand

RJ's screenshots live in `/Users/rhondajakub/Desktop/organized ss/` (macOS screencapture location is set to this folder). Filenames may be `Screenshot *.png`, `Screen Shot *.png`, `LWScreenShot *.png`, or UUID-named PNGs from other capture tools.

## How to parse `/ss [args]`

Argument string after `/ss`:
- **First token is a positive integer** → that's the count `N`. Everything after it is the instruction.
- **First token is not an integer** → `N = 1`. The whole arg string is the instruction.
- **No args at all** → `N = 1`, instruction = "explain what's in the screenshot."

Examples:
- `/ss` → newest 1, explain it
- `/ss huh` → newest 1, instruction = "huh" (explain it to me)
- `/ss 4` → newest 4, no specific instruction → explain them
- `/ss 3 make infographic plz` → newest 3, instruction = "make infographic plz"
- `/ss fix` → newest 1, instruction = "fix" (debug the code/design error shown)
- `/ss do this` → newest 1, instruction = "do this" (learn + remix for RJ's goals)

## Step 1 — Find the N most recent screenshots

Run this Bash command, substituting `N`:

```bash
ls -t ~/Desktop/"organized ss"/*.png ~/Desktop/"organized ss"/*.PNG 2>/dev/null | head -N
```

Show the user the list of files you found (filenames only, newest first) before reading them, so she can confirm you grabbed the right ones if anything looks off.

## Step 2 — Read the screenshots

Use the Read tool on each file path. The Read tool handles PNGs as images and Claude can see them visually.

## Step 3 — Act on the instruction

Map the instruction to behavior:

| Instruction pattern | Action |
|---|---|
| empty, `huh`, `what`, `explain`, `?` | Describe what's in the screenshot(s) clearly. If multiple, note how they relate. |
| `fix` | The screenshot shows an error: a code error message, a stack trace, a console log, or a UI/design bug (overlapping text, broken layout, wrong color). Identify the root cause, locate the relevant code in the current working directory, and edit the file to fix it. Explain the fix briefly. |
| `make infographic`, `infographic`, `combine`, `unified` | Synthesize content across all N screenshots into a single visual infographic. Default to an HTML/SVG file in the current working directory unless RJ specifies otherwise. |
| `do this`, `copy this`, `remix` | RJ saw something smart someone else did. Extract the underlying tactic/structure, then propose a goal-oriented version tailored to RJ (use memory: her interview pipeline, her writing voice, her current projects). Don't copy verbatim — remix for her outcomes. |
| `draft`, `reply`, `thank you`, etc. | Treat the screenshot as source material (an email, a message, a job post) and produce the requested artifact. |
| anything else | Take the instruction literally, using the screenshot(s) as context. |

## Step 4 — Use memory when relevant

For `do this` and other goal-oriented asks, check `~/.claude/projects/-Users-rhondajakub-Claude-for-Builders/memory/MEMORY.md` for what RJ is working on (active interviews, projects, voice/preferences) so the remix lands.

## Notes

- If no screenshots exist or `N` exceeds what's available, tell RJ what you found and proceed with what's there.
- Don't move, rename, or delete the screenshot files — they're RJ's originals.
- Keep responses tight. RJ uses `/ss` because she wants speed.
