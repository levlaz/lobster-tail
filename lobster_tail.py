#!/usr/bin/env python3
"""
Lobste.rs Story Opener (Python Version)
This script scrapes lobste.rs and opens each story in the default browser.
"""
import sys
import os
import platform
import requests
from bs4 import BeautifulSoup
import time
import webbrowser

print("🦞 Lobste.rs Story Opener (Python Version)")
print("========================================")

# Determine the open command or use webbrowser
open_cmd = None
system = platform.system().lower()
if system == "darwin":
    open_cmd = "open"
elif system == "linux":
    open_cmd = "xdg-open"
elif system == "windows":
    open_cmd = "start"

print(f"Detected OS: {system}")

print("Fetching stories from lobste.rs...")
try:
    resp = requests.get("https://lobste.rs", timeout=10)
    resp.raise_for_status()
except Exception as e:
    print(f"Error: Failed to fetch lobste.rs: {e}")
    sys.exit(1)

soup = BeautifulSoup(resp.text, "lxml")
story_links = soup.find_all("a", class_="u-url")

urls = []
for link in story_links:
    href = link.get("href")
    if href:
        if href.startswith("http"):
            urls.append(href)
        elif href.startswith("/"):
            urls.append(f"https://lobste.rs{href}")

urls = list(sorted(set(urls)))
story_count = len(urls)

if story_count == 0:
    print("No stories found. The website structure might have changed.")
    sys.exit(1)

print(f"Found {story_count} stories!\n")
print("Stories to open:")
for i, url in enumerate(urls, 1):
    print(f"{i}. {url}")
print()

if not open_cmd and not webbrowser.get():
    print(f"✅ Found {story_count} stories! Copy and paste the URLs above to open them in your browser.")
    sys.exit(0)

try:
    answer = input(f"Open all {story_count} stories in your browser? (y/N): ").strip().lower()
except KeyboardInterrupt:
    print("\nCancelled.")
    sys.exit(0)

if answer != "y":
    print("Cancelled.")
    sys.exit(0)

print("\nOpening stories...")
successful = 0
for i, url in enumerate(urls, 1):
    print(f"Opening {i}/{story_count}: {url}")
    try:
        if open_cmd:
            # Use OS command
            if system == "windows":
                os.system(f'start "" "{url}"')
            else:
                os.system(f'{open_cmd} "{url}"')
        else:
            webbrowser.open(url)
        successful += 1
    except Exception as e:
        print(f"Failed to open: {url} ({e})")
    time.sleep(0.5)

print(f"\n✅ Successfully opened {successful}/{story_count} stories!")
