---
name: build-career-bank
description: Build or improve the career bank in me/ - extract facts from an existing CV in me/cv_original/, interview the user to fill gaps (experience details, numbers, STAR stories, skills), and write profile.md, experience/*.md and stories.md. Use on first setup or "update my profile".
argument-hint: [optional: cv | stories | skills | all]
---

# /build-career-bank

Focus: $ARGUMENTS (default: all)

The career bank is the only source of truth for every document, so accuracy beats speed. Run in the main conversation (it's interactive).

1. **Extract:** read `me/questionnaire.md` answers first (they override the old CV where they differ, including items the user wants removed; delete those from the bank). Then if `me/cv_original/` has a CV (PDF/DOCX/TXT), read it fully. Draft updates to `me/profile.md` and one `me/experience/<file>.md` per role/project using the template in `me/experience/README.md`. Show the user what you extracted; write only after they confirm.
2. **Deepen:** for each experience file, ask up to 4 targeted questions to get what CVs usually lack: tools used, scale (budget, size, data volume, people), measurable results, what *they* personally did. Ask in small batches, not all at once. Accept "don't know" — never fill in guesses.
3. **Stories:** guide the user through STAR stories for the themes in `me/stories.md`, starting with the career story ("how did you get here, and why this field?"), then teamwork, problem-solving with data, failure, leadership. Draft each from their answers; they approve.
4. **Skills audit:** for each skill in the profile ask how they'd prove it in an interview (project, course, grade). Mark unproven ones as "familiar" rather than removing silently. Record skills the user never wants listed under "Never list".
5. **Dates and work rights:** check every date against transcripts or contracts (overlaps between study and jobs are easy to miss), and record the exact work-rights wording the user wants on applications.
6. **Report:** what's now complete, what's still TODO, and which missing items most often matter for the target roles in `config/search.md` (e.g. SQL evidence, a portfolio project, a dashboard).

Also useful at any time: after a new course module, project, or society role, run `/build-career-bank` to log it while it's fresh.
