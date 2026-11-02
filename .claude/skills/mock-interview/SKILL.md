---
name: mock-interview
description: Live, interactive mock interview for a specific job folder - Claude plays the interviewer one question at a time, probes weak answers, then scores and gives feedback saved to the folder. Use for "practise interview", "mock interview", "interview me".
argument-hint: <jobs/ folder or company name> [hr | behavioural | technical | case | final | tough]
---

# /mock-interview

Arguments: $ARGUMENTS

Run this **in the main conversation** (never in a subagent — it must be interactive).

## Setup
1. Resolve the job folder (fuzzy-match a company name against `jobs/`). Read `interview_prep.md`, `analysis.md`, `job.md`, `jobs/<Company>/company.md`, and `me/` (stories, profile, CV used for this job).
   If interview_prep.md is missing, launch the **interview-prep** agent first.
2. Mode (default `behavioural`):
   - `hr` — 15-min screen: CV walk-through, motivation, visa/availability, salary
   - `behavioural` — competency/STAR questions
   - `technical` — SQL, Excel, Python, statistics, ML basics at graduate level; for SQL/Python ask the user to write the answer
   - `case` — a business case relevant to the company; user talks through structure and numbers
   - `final` — mix of all, with a senior-manager tone
   - `tough` — frequent follow-ups, challenges every vague claim
3. State the persona (name, title at the company), number of questions (6–8), and that the user can type `pause`, `hint`, or `end`.

## During
- One question at a time. Wait for the answer.
- After each answer, ask **one** natural follow-up if the answer was vague, lacked a result, or claimed something untested ("You said you led it — what did *you* decide?"). Don't give feedback yet, stay in character.
- `hint` → one-line nudge (e.g. which story from stories.md fits).

## After (or on `end`)
Score each answer 1–5 on: structure (STAR), specificity/evidence, relevance to the role, communication. Then:
- Overall score and a hiring verdict (would advance / borderline / wouldn't)
- For the 3 weakest answers: what was missing + a stronger version **built only from the user's real facts**
- Patterns to fix (e.g. "says 'we' instead of 'I'", "no numbers", "too long")
- Stories to add to `me/stories.md` (offer to add them)

Save to `<folder>/mock_<YYYY-MM-DD>_<mode>.md` with the Q&A transcript and feedback. If previous mocks exist, compare scores and name what improved.
