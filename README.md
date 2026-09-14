# CVDesigner

CVDesigner is a VS Code skill and small set of standard-library Python helpers
for building evidence-backed job application materials.

The general LaTeX layout is available at
`templates/cv-template.tex`. It contains placeholders only and does not include
the example CV's personal data.

## Workflow

Use the `cv-job-application` skill in `.github/skills/cv-job-application/SKILL.md`.
It collects a current role first, then gathers background and proposes follow-up
questions. It stores only confirmed candidate facts, waits for a job description,
maps requirements to evidence, asks clarification questions, and generates LaTeX
only after those questions are answered.

The attached or existing CV is not imported automatically. Candidate data must be
entered and confirmed by the user.

## Quick start

From the CVDesigner directory:

```powershell
python scripts/profile_store.py init --output data/profile.json
python scripts/profile_store.py validate --file data/profile.json
python scripts/job_description.py ingest --url <JOB_DESCRIPTION_URL> --output data/job-description.json
python scripts/render_latex.py --profile data/profile.json --output output/cv.tex
```

Use `--file` instead of `--url` when the job description is stored locally. The
render script intentionally omits empty sections; tailoring and final wording are
controlled by the skill after the user confirms missing details.

The scripts require Python 3.10 or newer and have no third-party dependencies.