#!/usr/bin/env python3
"""Fridge Roast: One Line, Biggest Laugh - a make.fun entry.

``python3 main.py`` writes the roast to ``entry.txt`` with no trailing
newline. The gate is 1-200 characters of UTF-8 text, not only
whitespace, so the line is validated first and the written file is
checked byte for byte before the script reports success.
"""

import os
import sys

ENTRY = "The fridge camera caught me eating the last slice at 2 a.m. and emailed me a lecture about portion control."
LIMIT = 200


def entry_path():
    """Resolve the output file from the grader's dir, else the cwd."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR") or "."
    return os.path.join(directory, "entry.txt")


def validate(line):
    """Return the line as UTF-8 bytes, or exit if it fails the gate."""
    if not line.strip():
        raise SystemExit("entry must not be blank or only whitespace")
    if len(line) > LIMIT:
        raise SystemExit(
            "entry is %d characters, above the %d limit" % (len(line), LIMIT)
        )
    return line.encode("utf-8")


def run():
    data = validate(ENTRY)
    path = entry_path()
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "wb") as out:
        out.write(data)
    with open(path, "rb") as check:
        if check.read() != data:
            raise SystemExit("entry.txt read-back does not match the entry")
    return path


def self_test():
    """Round-trip the entry through a scratch directory."""
    import tempfile

    previous = os.environ.get("MAKEFUN_OUTPUT_DIR")
    with tempfile.TemporaryDirectory() as scratch:
        os.environ["MAKEFUN_OUTPUT_DIR"] = scratch
        try:
            path = run()
            with open(path, "rb") as check:
                data = check.read()
        finally:
            if previous is None:
                os.environ.pop("MAKEFUN_OUTPUT_DIR", None)
            else:
                os.environ["MAKEFUN_OUTPUT_DIR"] = previous
    assert data == ENTRY.encode("utf-8"), "written bytes differ from ENTRY"
    assert data[-1:] != b"\n", "no trailing newline allowed"
    assert data.count(b"\n") == 0, "entry must be a single line"
    assert len(data) == 107, "expected 107 bytes, got %d" % len(data)
    print("self-test OK: entry.txt holds the 107-character roast exactly")


def main(argv):
    if "--self-test" in argv or "--check" in argv:
        validate(ENTRY)
        self_test()
        return 0
    path = run()
    print("wrote %s (%d characters, no trailing newline)" % (path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
