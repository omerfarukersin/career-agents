---
name: job-status
description: Dashboard of the job search - pipeline counts, upcoming deadlines, follow-ups due, recurring skill gaps across all analysed jobs with a learning plan. Use for "status", "what's next", "what should I do today", "skill gaps".
argument-hint: [optional: gaps | deadlines | followups]
---

# /job-status

Focus: $ARGUMENTS

Read `tracker/tracker.csv` and all `jobs/**/analysis.md`. Today's date is from the environment.

Report (skip empty sections):
1. **Today's actions:** rows with `next_action_date` ≤ today, and deadlines within 7 days not yet `applied`. One line each with the exact action.
2. **Pipeline:** counts per status; response rate (interview ÷ applied) once ≥5 applied.
3. **Deadlines (next 30 days).**
4. **Follow-ups:** `applied` rows with no update for ≥7 days → offer to draft a polite follow-up to the contact/recruiter (save into that folder's outreach.md; user sends).
5. **Recurring skill gaps:** count unsupported must-haves and ❌ keywords across all analyses. For any gap appearing in ≥30% of jobs: why it matters, a 1–3 week plan with free resources (e.g. SQL, Power BI PL-300 content, Tableau, dbt, cloud fundamentals), and a small portfolio project idea that would let the user honestly claim it. Offer to log completed learning into `me/`.
6. **Stale data:** job folders with status `found`/`analysed` older than 21 days whose deadline has passed → suggest marking withdrawn/skipped.

If `config/airtable.md` says `status: configured`, sync differences from tracker.csv to Airtable and report what changed.
