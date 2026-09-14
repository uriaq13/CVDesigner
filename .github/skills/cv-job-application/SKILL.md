---
name: cv-job-application
description: "Use when building a CV, cover letter, interview preparation package, or tailoring application materials to a job description. Collects a user's role and background, stores only supplied facts, waits for a job description, identifies evidence and gaps, asks clarifying questions, and produces evidence-backed LaTeX only after approval."
---

# CV and Job Application Workflow

This skill is a staged workflow. Do not skip a gate and do not infer facts about the user.

## Source-of-truth rules

- Treat `data/profile.json` as the only source of candidate facts.
- Treat `data/job-description.json` as the only source of job-post facts.
- Never use an attached CV, an older draft, a web profile, or a plausible assumption as profile data unless the user explicitly asks to import it and confirms the imported fields.
- Preserve uncertainty with `unknown`, `needs_confirmation`, or an empty value. Do not turn missing information into a claim.
- Do not generate a CV, cover letter, or interview package during intake.

## Stage 1: establish direction

If no current role or target direction has been provided, ask first:

> What is your current role, professional area, or target direction? Examples: software engineering, data analysis, quality assurance, design, operations, research, or another field.

Accept a current role, target role, career transition, student status, or another clear direction. Save the answer as `current_role` and/or `target_roles`; do not require a conventional job title.

Stop after asking this question if the answer is not available.

## Stage 2: collect the profile

Once direction is known, ask for the following in one structured intake. The user may answer in multiple messages:

- Education or equivalent background: institution, program, dates, focus, relevant coursework.
- Professional experience: employer, title, location, dates, responsibilities, outcomes, tools, and measurable impact.
- Projects: optional; context, contribution, technologies, result, and links.
- Certifications, licenses, courses, publications, talks, awards, or volunteer work.
- Skills: technical, domain, interpersonal, languages, proficiency, and evidence.
- Portfolio, GitHub, LinkedIn, website, or other links.
- Location, work authorization, remote/onsite preference, and relocation constraints if relevant.
- Target industries, role level, preferred language, and CV length if known.

Then propose these additional questions before saving the completed profile:

- Which accomplishments are you most proud of?
- Which outcomes can be quantified with time, cost, quality, revenue, scale, or risk reduction?
- Which tools or skills should be emphasized or de-emphasized?
- Are there employment gaps, career changes, confidential projects, or naming restrictions to handle?
- Which interview formats are expected: behavioral, technical, case, portfolio, or panel?
- What tone and countries' conventions should the application follow?

Ask the user to answer what applies and explicitly allow them to say `skip` or `unknown`. Store the answers with `python scripts/profile_store.py validate --file data/profile.json` after the user confirms the profile. Do not create candidate data on the user's behalf.

## Stage 3: wait state

After the profile is saved, acknowledge that intake is complete and wait. Do not generate a CV or any other material until the user supplies either:

- a job-description URL; or
- the full job-description text or a file containing it.

For a URL or text, run:

```powershell
python scripts/job_description.py ingest --url <URL> --output data/job-description.json
python scripts/job_description.py ingest --file <PATH> --output data/job-description.json
python scripts/job_description.py ingest --text "<JOB_DESCRIPTION_TEXT>" --output data/job-description.json
```

Use only one input mode. For long pasted text, a file is usually easier to review.

## Stage 4: evidence-first analysis

After receiving the job description:

1. Extract the role title, responsibilities, requirements, preferred qualifications, location, employment details, and application constraints.
2. Map each requirement to profile evidence, marking each as `supported`, `partially_supported`, `missing`, or `unclear`.
3. Produce a first draft plan, not a final CV: proposed headline, section order, evidence-backed bullet candidates, keywords, and gaps.
4. Ask focused questions for every material `missing` or `unclear` item and for any metric, date, scope, or ownership needed to make a claim accurate.
5. Do not fill gaps with generic claims, inferred seniority, invented metrics, or guessed technologies.

The first draft may be saved as `data/application-draft.md`, but it must clearly label unsupported items as questions or omissions.

## Stage 5: final materials

Only after the user answers the clarification questions:

- Update the profile with confirmed facts.
- Generate the CV in LaTeX using `python scripts/render_latex.py --profile data/profile.json --output output/cv.tex`.
- Keep wording faithful to the confirmed data and tailor ordering and emphasis to the job description.
- Generate a cover letter or interview preparation document only when explicitly requested.
- Before presenting output, run the script validation and report any omitted sections or unresolved questions.

## Data commands

Initialize a blank, non-personal schema:

```powershell
python scripts/profile_store.py init --output data/profile.json
```

Validate candidate data without changing it:

```powershell
python scripts/profile_store.py validate --file data/profile.json
```

The helper scripts are intentionally standard-library-only and do not fetch or infer candidate information beyond the supplied input.
