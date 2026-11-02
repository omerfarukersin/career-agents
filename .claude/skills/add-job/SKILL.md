---
name: add-job
description: Full application pipeline for one job - ingest posting (URL, pasted text, inbox file, or existing folder), analyse fit, then in parallel research the company, tailor CV and cover letter, find contacts and prepare interview; critique and revise; build PDFs; update tracker. Use when the user shares a job or says "apply to", "tailor for", "add this job".
argument-hint: <job URL | pasted text | inbox file | existing jobs/ folder> [notes]
---

> Whenever a subagent returns ```file:<path>``` blocks (it was blocked from writing), save each block verbatim to that path before continuing.

# /add-job — orchestrate one application

Input: $ARGUMENTS

You are the orchestrator. Delegate work to the subagents in `.claude/agents/`; you handle checkpoints with the user, sequencing, and the tracker. Follow CLAUDE.md rules.

## 0. Preconditions
- If `me/profile.md` still has TODOs in Contact, Education or Technical skills, or `me/experience/` has no files besides README: tell the user which gaps weaken the output and offer `/build-career-bank`. Continue only if they say so.

## 1. Ingest
- Before spending effort, check the posting is still live (postings often close before their stated deadline). Skip this for pasted postings and placeholder URLs.
- If the input is an existing `jobs/...` folder with job.md, use it. If the tracker has no row for it, add one (id and fields as in CLAUDE.md, status `found`).
- If the folder has no `status.md`, copy `engine/templates/job/status.md` into it.
- Otherwise launch **job-scout** in single-job mode with the URL/text/file. Any extra company documents the user attached → save into the job folder and reference them under "Extra documents" in job.md.
- If the company already has other role folders, mention it — each role still gets its own CV and letter.

## 2. Analyse
Launch **job-analyst** on the folder. Show the user: fit score, verdict, top matches, top gaps, deadline, required documents.

## 3. ✋ Checkpoint 1
Ask the user: proceed with full tailoring? Offer: proceed / proceed but skip networking or interview prep / skip this job. If fit < threshold in config/search.md, say so clearly and recommend skip unless there's a reason (dream company, referral). Also ask for anything the analyst flagged as missing from the career bank that the user can quickly confirm.
On skip: tracker status `skipped`, stop.
If the analyst flagged an application limit (one application per cycle, or only the first role counts), tell the user before they choose.

## 4. Parallel build
Tracker status `approved`. Launch in parallel (one message, multiple Agent calls):
- **company-researcher** (skip if company.md is fresh)
- **cv-writer**
- **networker** (unless skipped)
- **interview-prep** (unless skipped)

Then launch **cover-letter-writer** (needs company.md, so after the researcher finishes; it can run alongside the others if company.md already existed). Skip the letter only if the posting clearly says no cover letter is accepted.

## 5. Critique loop
Launch **recruiter-critic**. If REVISE: pass critique.md to cv-writer and/or cover-letter-writer to revise, then critique again. Max 2 revision rounds; if still REVISE, report the remaining issues to the user instead of looping.

## 6. ✋ Checkpoint 2
Tracker status `drafted`. Give the user:
- links to `cv.pdf`, `cover_letter.pdf`, `outreach.md`, `interview_prep.md`
- critic scores, ATS keyword coverage, any claims needing their confirmation
- top 3 people to contact and the first message to send
- deadline and exact next steps to submit
Before handing over, make the upload-safe copies: `python3 engine/scripts/make_upload_pdf.py <folder>/cv.pdf <folder>/<First>_<Last>_CV.pdf` (same for the letter).
Ask for edits. Apply edits via the writers (or directly for tiny changes, then rebuild with `engine/scripts/build_pdf.sh`). When the user approves → status `final`.

## 7. Record
Update `tracker/tracker.csv` (and Airtable if `config/airtable.md` says `status: configured`): status, fit, deadline, folder, contacts, next_action (e.g. "submit by <date>", "send note to <name>"), next_action_date. Append to `<folder>/status.md`. Save every form question and the exact answer the user submitted in `<folder>/application_answers.md`. When the user says they applied → status `applied`, applied_date, next_action "follow up" +7 days.
Add any new reusable form answers the user wrote to `me/answer_bank.md`.
