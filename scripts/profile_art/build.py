#!/usr/bin/env python3
"""Regenerate the artwork used by README.md.

    pip install fonttools brotli
    python3 scripts/profile_art/build.py

Writes assets/header.svg, education.svg, research.svg and footer.svg. Text and layout
live in the modules next to this file; fonts are downloaded once into .fonts/.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cards  # noqa: E402
import footer  # noqa: E402
import header  # noqa: E402

ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "assets"))


def main():
    os.makedirs(ASSETS, exist_ok=True)
    for name, make in (("header", header.build), ("education", cards.education), ("research", cards.research), ("footer", footer.build)):
        svg = make()
        path = os.path.join(ASSETS, f"{name}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"{os.path.relpath(path)}  {len(svg.encode()) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
