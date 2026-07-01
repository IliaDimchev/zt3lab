#!/usr/bin/env python3

import argparse
import os
from pathlib import Path


TREE_CHARS = "│├└─"


def parse_tree(lines):
    """
    Converts an ASCII tree into a list of paths.
    Returns:
        [(Path(...), is_dir)]
    """

    stack = []
    result = []

    for raw in lines:
        line = raw.rstrip()

        if not line.strip():
            continue

        # Root folder
        if line.endswith("/") and not any(c in line for c in TREE_CHARS):
            root = line.rstrip("/")
            stack = [root]
            result.append((Path(root), True))
            continue

        if "── " not in line:
            continue

        prefix, name = line.split("── ", 1)

        depth = (
            prefix.count("│   ")
            + prefix.count("    ")
        )

        name = name.rstrip()

        while len(stack) > depth + 1:
            stack.pop()

        is_dir = name.endswith("/")

        clean = name.rstrip("/")

        path = Path(*stack, clean)

        result.append((path, is_dir))

        if is_dir:
            stack.append(clean)

    return result


def create(paths):
    for path, is_dir in paths:
        if is_dir:
            path.mkdir(parents=True, exist_ok=True)
            print(f"[DIR ] {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)
            print(f"[FILE] {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Create folders/files from an ASCII tree."
    )

    parser.add_argument(
        "file",
        nargs="?",
        help="Tree file. If omitted, read from stdin."
    )

    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            lines = f.readlines()
    else:
        print("Paste the tree below. Finish with Ctrl+D (Linux/macOS) or Ctrl+Z then Enter (Windows):")
        import sys
        lines = sys.stdin.readlines()

    paths = parse_tree(lines)
    create(paths)


if __name__ == "__main__":
    main()
