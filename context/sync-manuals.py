#!/usr/bin/env python3
"""Generate `AGENTS.md` (OpenCode's manual) from `CLAUDE.md` (Claude Code's).

The two manuals are the same document. Regenerating one from the other by hand
drifted, so the regeneration is a script. A difference can exist in exactly two
places, and anything else is drift:

- the SUBSTITUTIONS list below;
- OPENCODE_APPENDIX, a section appended to AGENTS.md only. OpenCode has no
  per-user memory and follows pointers less reliably than Claude Code, so it
  gets an explicit step-by-step procedure. It is a routing layer: it says *when*
  to read an owner and names it, and restates a rule only as a one-line trigger.

Run from the repository root after editing either source:

    python3 context/sync-manuals.py

It fails rather than silently overwriting if a source is missing or a
substitution no longer matches.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "CLAUDE.md")
TARGET = os.path.join(ROOT, "AGENTS.md")
OPENCODE_APPENDIX = os.path.join(ROOT, "context", "manual-opencode.md")

# Every intentional difference between the two runtimes, in order. Anything
# else must not differ: add it here deliberately, with a reason, or fix the
# manual instead.
SUBSTITUTIONS = [
    ("# CLAUDE.md\n", "# AGENTS.md\n"),
    (
        "**`AGENTS.md` is generated from this file** by `context/sync-manuals.py`",
        "**This file is generated from `CLAUDE.md`** by `context/sync-manuals.py`",
    ),
]


def main():
    for path in (SOURCE, OPENCODE_APPENDIX):
        if not os.path.exists(path):
            sys.exit(f"missing {path}")

    text = open(SOURCE, encoding="utf-8").read()
    for old, new in SUBSTITUTIONS:
        if old not in text:
            sys.exit(f"substitution no longer matches, fix the script: {old!r}")
        text = text.replace(old, new)

    appendix = open(OPENCODE_APPENDIX, encoding="utf-8").read()
    text = text.rstrip("\n") + "\n\n" + appendix.rstrip("\n") + "\n"

    open(TARGET, "w", encoding="utf-8").write(text)
    print(f"wrote {os.path.relpath(TARGET, ROOT)} from {os.path.relpath(SOURCE, ROOT)} "
          f"({len(SUBSTITUTIONS)} substitution(s), plus "
          f"{os.path.relpath(OPENCODE_APPENDIX, ROOT)})")


if __name__ == "__main__":
    main()
