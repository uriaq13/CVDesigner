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

## System Requirements

- Visual Studio Code with GitHub Copilot Chat or another environment that can
	load the `.github/skills/cv-job-application/SKILL.md` workflow.
- Python 3.10 or newer available on `PATH` as `python`.
- Windows 10/11, macOS, or Linux for the standard-library Python helpers. The
	documented commands use PowerShell syntax; use the equivalent shell commands
	on other operating systems.
- Internet access only when ingesting a job description from a URL. Local files
	and pasted text do not require network access.
- Read and write access to the CVDesigner directory, including `data/` and
	`output/`.
- A LaTeX distribution such as MiKTeX or TeX Live is optional for generating
	`.tex` files and required for PDF compilation and page-count verification.

## Requirements

- Candidate facts must come from `data/profile.json` and job-post facts must come
	from `data/job-description.json`.
- The intake must explicitly collect and confirm the candidate's full name,
	professional email, phone number, and city/country. Missing contact details
	remain unresolved; they are never inferred from attachments, file paths, or
	account metadata.
- Education, experience, projects, skills, dates, tools, outcomes, proficiency,
	links, work preferences, and restrictions must be supplied or confirmed by the
	candidate.
- Missing, uncertain, or intentionally skipped information must remain empty or
	use `unknown`/`needs_confirmation`. Skipped items must be omitted from final
	application materials.
- A job description must be supplied as a URL, local file, or text before
	tailoring. Job-board pages such as LinkedIn may contain navigation and sign-in
	HTML; the visible role description must be reviewed before requirements are
	mapped.
- Every job requirement must be marked `supported`, `partially_supported`,
	`missing`, or `unclear` before final wording is prepared. Metrics, technologies,
	seniority, ownership, and outcomes must not be invented.
- Final materials require a validated profile, confirmed contact details, review
	of the generated `output/cv.tex`, and a report of any omitted or unresolved
	items. Compile the LaTeX and verify page count when a local compiler is
	available.

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

The renderer accepts the profile's confirmed experience, education, skills, and
project fields and escapes common LaTeX-special characters. Inspect the generated
file before submitting it; a successful render command does not by itself verify
that every intended section or field is present.

## LaTeX setup

For Windows, MiKTeX is the recommended local LaTeX distribution for this project:

```powershell
winget install MiKTeX.MiKTeX
```

TeX Live is also supported when a larger, fully preinstalled distribution is
preferred. If no LaTeX compiler is installed, the CV can still be rendered as
`.tex`, but PDF compilation and page-count verification remain incomplete.

The scripts require Python 3.10 or newer and have no third-party dependencies.