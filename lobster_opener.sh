#!/bin/bash

# Lobste.rs Story Opener (Bash Version)
# This script scrapes lobste.rs and opens each story in the default browser

set -e

echo "🦞 Lobste.rs Story Opener (Bash Version)"
echo "========================================"

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Warning: This script is designed for macOS. The 'open' command may not work on other systems."
fi

# Check if required tools are available
if ! command -v curl &> /dev/null; then
    echo "Error: curl is required but not installed."
    exit 1
fi

if ! command -v grep &> /dev/null; then
    echo "Error: grep is required but not installed."
    exit 1
fi

# Temporary file to store the HTML
temp_file=$(mktemp)
trap "rm -f $temp_file" EXIT

echo "Fetching stories from lobste.rs..."

# Fetch the lobste.rs front page
if ! curl -s -L "https://lobste.rs" > "$temp_file"; then
    echo "Error: Failed to fetch lobste.rs"
    exit 1
fi

# Extract story URLs using grep and sed
# Look for links with class="u-url" which are the story titles
story_urls=$(grep -o 'href="[^"]*"[^>]*class="u-url"' "$temp_file" | \
             sed 's/href="//g' | \
             sed 's/".*//g' | \
             sort -u)

# Convert relative URLs to absolute URLs
absolute_urls=""
while IFS= read -r url; do
    if [[ $url == http* ]]; then
        absolute_urls="$absolute_urls$url"$'\n'
    elif [[ $url == /* ]]; then
        absolute_urls="${absolute_urls}https://lobste.rs$url"$'\n'
    fi
done <<< "$story_urls"

# Remove empty lines and count stories
story_count=$(echo "$absolute_urls" | grep -c "^http" || echo "0")

if [[ $story_count -eq 0 ]]; then
    echo "No stories found. The website structure might have changed."
    exit 1
fi

echo "Found $story_count stories!"
echo

# Show the URLs that will be opened
echo "Stories to open:"
counter=1
while IFS= read -r url; do
    if [[ -n "$url" ]]; then
        echo "$counter. $url"
        ((counter++))
    fi
done <<< "$absolute_urls"

echo
read -p "Open all $story_count stories in your browser? (y/N): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo
echo "Opening stories..."

# Open each URL
counter=1
successful=0
while IFS= read -r url; do
    if [[ -n "$url" ]]; then
        echo "Opening $counter/$story_count: $url"
        if open "$url" 2>/dev/null; then
            ((successful++))
        else
            echo "Failed to open: $url"
        fi
        ((counter++))
        # Small delay to avoid overwhelming the browser
        sleep 0.5
    fi
done <<< "$absolute_urls"

echo
echo "✅ Successfully opened $successful/$story_count stories!"