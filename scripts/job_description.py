#!/usr/bin/env python3
"""Store a supplied job description without inventing or summarizing facts."""

import argparse
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def read_source(url: str | None, file: Path | None, text: str | None) -> tuple[str, str]:
    provided = sum(value is not None for value in (url, file, text))
    if provided != 1:
        raise SystemExit("Provide exactly one of --url, --file, or --text")
    if url:
        request = urllib.request.Request(url, headers={"User-Agent": "CVDesigner/1.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            return url, response.read().decode(response.headers.get_content_charset() or "utf-8")
    if file:
        return str(file), file.read_text(encoding="utf-8")
    assert text is not None
    return "inline", text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ingest", choices=["ingest"])
    parser.add_argument("--url")
    parser.add_argument("--file", type=Path)
    parser.add_argument("--text")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source, text = read_source(args.url, args.file, args.text)
    if not text.strip():
        raise SystemExit("The supplied job description is empty")
    payload = {
        "source": source,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "text": text,
        "analysis_status": "not_analyzed",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Stored job description at {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
