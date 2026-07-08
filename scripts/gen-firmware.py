#!/usr/bin/env python3
"""Regenerate content/firmware/_index.md from files in static/firmware/."""

import datetime
from pathlib import Path

FIRMWARE_DIR = Path("static/firmware")
INDEX_FILE = Path("content/firmware/_index.md")

def human_size(n):
    for unit in ("B", "KB", "MB"):
        if n < 1024:
            return f"{n:.0f} {unit}"
        n /= 1024
    return f"{n:.1f} MB"

# Preserve existing body content (everything after closing +++)
existing = INDEX_FILE.read_text() if INDEX_FILE.exists() else ""
parts = existing.split("+++", 2)
body = parts[2].lstrip("\n") if len(parts) > 2 else "Firmware downloads.\n"

all_files = sorted((f for f in FIRMWARE_DIR.iterdir() if f.is_file()), key=lambda f: f.name)

entries = []
for f in all_files:
    stat = f.stat()
    size = human_size(stat.st_size)
    date = datetime.date.fromtimestamp(stat.st_mtime).isoformat()
    entries.append(f'[[extra.files]]\nname = "{f.name}"\nsize = "{size}"\ndate = "{date}"')

frontmatter = "\n".join([
    '# THIS IS A GENERATED FILE; DO NOT EDIT',
    'title = "Firmware"',
    'template = "firmware.html"',
    "render = true",
    "[extra]",
    "\n\n".join(entries),
])

INDEX_FILE.write_text(f"+++\n{frontmatter}\n+++\n\n{body}")
print(f"Updated {INDEX_FILE} ({len(all_files)} files)")
