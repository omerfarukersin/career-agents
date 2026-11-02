# Adapting to another country or field

The agents are country-neutral; they read conventions from `config/`. The shipped defaults are an Ireland pack for graduate data, analytics, AI and consulting roles.

## Another country
Edit `config/search.md`:
1. **Location:** country, preferred and acceptable cities.
2. **Country conventions:** CV length, photo and date-of-birth norms, spelling, cover-letter length and sign-off, how grades are read, local business press. For example, Germany often expects a photo and a longer *Lebenslauf*; the US expects a one-page résumé and "Sincerely".
3. **Timing notes:** when graduate programmes open and close.
4. **Eligibility rules:** the clauses employers use (citizenship lists, permits, clearance) and anything public bodies require.

Then edit `config/sources.md` section 3 (job boards for that country) and replace `config/target_companies.csv` with employers you care about. The `ats` and `ats_slug` columns can be left blank; the scout detects them on its first run and writes them back.

If the country uses US-style résumés, also adjust the section order in `engine/templates/cv.tex`.

## Another field or level
- Rewrite the role-family tiers in `config/search.md`; the analyst scores against them.
- For experienced hires, change the level filter in `config/search.md` and the section order in `.claude/agents/cv-writer.md` (Experience before Education).
- The technical question list in `.claude/agents/interview-prep.md` and the modes in `/mock-interview` lean towards data roles; edit them for your field.

## Contributing a country pack
A pull request that adds `docs/packs/<country>.md` (conventions, timing, eligibility, boards) is welcome.
