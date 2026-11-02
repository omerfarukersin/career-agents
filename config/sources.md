# Job sources (scout reads this)

Use in this order. Never log into any account; never scrape LinkedIn pages. Respect each site's terms of use and robots rules.

## 1. Public ATS feeds (most reliable): companies in `target_companies.csv`
| ATS | Public endpoint |
|---|---|
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true` |
| Lever | `https://api.lever.co/v0/postings/<slug>?mode=json` |
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/<slug>` |
| SmartRecruiters | `https://api.smartrecruiters.com/v1/companies/<slug>/postings` |
| Workable | `https://apply.workable.com/api/v1/widget/accounts/<slug>` |
| Workday (myworkdayjobs.com) | POST `https://<host>/wday/cxs/<tenant>/<site>/jobs` with JSON `{"appliedFacets":{},"limit":20,"offset":0,"searchText":"<city>"}` |
| Oracle Recruiting Cloud | `https://<host>/hcmRestApi/resources/latest/recruitingCEJobRequisitions?finder=findReqs;siteNumber=<site>,keyword=<city>` |
| Microsoft (Eightfold) | `https://apply.careers.microsoft.com/api/pcsx/search?domain=microsoft.com&location=<country>&start=N&num=10&filter_seniority=Entry` |
| Google | no API; results pages list job links in plain HTML; fetch them |
| Pinpoint | `https://<slug>.pinpointhq.com/postings.json` |
| Recruitee | `https://<slug>.recruitee.com/api/offers/` |
| SuccessFactors / Taleo / other | no stable public API; use the careers page or web search |

When `ats` is blank in the CSV, detect it from the careers page (links to greenhouse.io, lever.co, ashbyhq.com, myworkdayjobs.com...) and write it back. If an official page returns 403, retry once with ordinary browser headers before calling it unavailable.

## 2. Job-alert emails (manual forward)
The user sets job alerts (LinkedIn, Indeed, boards) and saves or forwards them to `inbox/`. The scout parses them there.

## 3. Graduate job boards (Ireland pack)
- gradireland.com (aggregator; can lag the employer's own ATS and sometimes shows no deadline, so always open the employer link)
- the user's university careers service (paste listings into `inbox/`)
- prosple / targetjobs Ireland
- irishjobs.ie, jobs.ie
- indeed.ie (via web search results)

## 4. General web search
Queries such as `"graduate programme" 2027 Dublin analytics`, `"business analyst" graduate Dublin`, `site:<careers domain> graduate`.

## Dedup
A job is the same if company + normalised title + location match, or the posting URL matches. Check `tracker/tracker.csv` before creating a folder.

## Liveness
Postings are often pulled before their stated deadline. Before an application day, re-open every posting you plan to apply to.
