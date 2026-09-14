#!/usr/bin/env python3
"""Render a conservative, evidence-only CV from a confirmed profile JSON."""

import argparse
import json
from pathlib import Path
from typing import Any


def latex(value: Any) -> str:
    replacements = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}"}
    return "".join(replacements.get(character, character) for character in str(value))


def render_section(title: str, entries: list[str]) -> str:
    if not entries:
        return ""
    return "\\section*{" + latex(title) + "}\n" + "\n".join(entries) + "\n"


def render_contact_line(contact: dict[str, Any]) -> str:
    values = [contact.get(key) for key in ("email", "phone", "location") if contact.get(key)]
    values.extend(contact.get("links", []))
    return latex(" \\quad ".join(values)) if values else ""


def render(profile: dict[str, Any]) -> str:
    contact = profile.get("contact", {})
    name = contact.get("name") or "Candidate Name"
    header = [
        r"\documentclass[a4paper,10pt]{article}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{geometry}",
        r"\usepackage{enumitem}",
        r"\usepackage[hidelinks]{hyperref}",
        r"\usepackage{parskip}",
        r"\usepackage{titlesec}",
        r"\geometry{top=1.25cm,bottom=1.25cm,left=1.25cm,right=1.25cm}",
        r"\setlength{\parindent}{0pt}",
        r"\linespread{0.97}",
        r"\titlespacing*{\section}{0pt}{0.5em}{0.25em}",
        r"\setlist[itemize]{leftmargin=*,topsep=1pt,partopsep=0pt,parsep=0pt,itemsep=1pt}",
        r"\begin{document}",
        r"\begin{center}",
        f"{{\\LARGE\\textbf{{{latex(name)}}}}}\\\\",
    ]
    contact_line = render_contact_line(contact)
    if contact_line:
        header.extend([r"\small", contact_line + r"\\"])
    header.extend([r"\end{center}", ""])

    sections = [render_section("Professional Summary", [latex(profile.get("summary"))] if profile.get("summary") else [])]
    experience = []
    for item in profile.get("experience", []):
        title = ", ".join(str(item.get(key)) for key in ("title", "employer", "location") if item.get(key))
        dates = latex(item.get("dates", ""))
        bullet_values = item.get("bullets") or item.get("responsibilities", [])
        bullets = [r"\item " + latex(bullet) for bullet in bullet_values if bullet]
        if title:
            line = r"\textbf{" + latex(title) + "}"
            if dates:
                line += r"\hfill \textit{" + dates + "}"
            experience.append(line + ("\n\\begin{itemize}\n" + "\n".join(bullets) + "\n\\end{itemize}" if bullets else ""))
    sections.append(render_section("Experience", experience))

    education = []
    for item in profile.get("education", []):
        degree = item.get("degree") or item.get("program")
        line = ", ".join(str(value) for value in (degree, item.get("institution")) if value)
        if line:
            education_line = r"\textbf{" + latex(line) + "}"
            if item.get("dates"):
                education_line += r"\hfill \textit{" + latex(item["dates"]) + "}"
            education.append(education_line)
        details = item.get("details") or item.get("focus")
        if details:
            education.append(latex(details))
    sections.append(render_section("Education", education))

    skills = []
    for category, values in profile.get("skills", {}).items():
        if values:
            skills.append(r"\textbf{" + latex(category.title()) + r":} " + latex(", ".join(values)) + r"\\")
    sections.append(render_section("Skills", skills))

    projects = []
    for item in profile.get("projects", []):
        description = item.get("result") or item.get("contribution")
        line = ": ".join(str(value) for value in (item.get("name"), description) if value)
        if line:
            projects.append(r"\textbf{" + latex(line) + "}")
    sections.append(render_section("Projects", projects))
    return "\n".join(header + sections + [r"\end{document}", ""])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(profile), encoding="utf-8")
    print(f"Rendered evidence-only LaTeX at {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
