#!/usr/bin/env python3
"""Render an SVG to PNG with headless Chrome or Chromium.

Usage: render.py diagram.svg [diagram.png] [--scale 2]

The canvas size is read from the SVG width and height attributes. Use scale 1
for a quick visual check and scale 2 for documents.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys


def find_browser():
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        path = shutil.which(name)
        if path:
            return path
    mac = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    return mac if os.path.exists(mac) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg")
    ap.add_argument("png", nargs="?")
    ap.add_argument("--scale", type=float, default=2)
    a = ap.parse_args()

    svg = os.path.abspath(a.svg)
    png = os.path.abspath(a.png or os.path.splitext(svg)[0] + ".png")
    head = open(svg, encoding="utf-8").read(2000)
    w = re.search(r'<svg[^>]*\swidth="(\d+)', head)
    h = re.search(r'<svg[^>]*\sheight="(\d+)', head)
    if not (w and h):
        sys.exit("The SVG needs numeric width and height attributes")

    browser = find_browser()
    if browser:
        cmd = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
               f"--force-device-scale-factor={a.scale:g}", f"--window-size={w.group(1)},{h.group(1)}",
               f"--screenshot={png}", f"file://{svg}"]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif shutil.which("rsvg-convert"):
        subprocess.run(["rsvg-convert", "-z", f"{a.scale:g}", "-o", png, svg], check=True)
    else:
        sys.exit("No renderer found. Install Google Chrome, Chromium or rsvg-convert (librsvg).")
    print(png)


if __name__ == "__main__":
    main()
