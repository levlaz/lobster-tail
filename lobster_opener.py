#!/usr/bin/env python3
"""
Lobste.rs Story Opener

This script scrapes the front page of lobste.rs and opens each story
in the default browser on macOS.
"""

import requests
from bs4 import BeautifulSoup
import subprocess
import time
import sys
from urllib.parse import urljoin

def get_lobsters_stories():
    """
    Scrape the front page of lobste.rs and extract story URLs.
    
    Returns:
        list: List of story URLs
    """
    try:
        # Send GET request to lobste.rs
        response = requests.get('https://lobste.rs', timeout=10)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all story links
        # Stories on lobste.rs are in <a> tags with class "u-url"
        story_links = []
        
        # Look for story titles which are typically in <a> tags within story containers
        stories = soup.find_all('div', class_='story')
        
        for story in stories:
            # Find the title link within each story
            title_link = story.find('a', class_='u-url')
            if title_link and title_link.get('href'):
                href = title_link.get('href')
                # Convert relative URLs to absolute URLs
                if href.startswith('/'):
                    full_url = urljoin('https://lobste.rs', href)
                else:
                    full_url = href
                story_links.append({
                    'title': title_link.get_text(strip=True),
                    'url': full_url
                })
        
        return story_links
        
    except requests.RequestException as e:
        print(f"Error fetching lobste.rs: {e}")
        return []
    except Exception as e:
        print(f"Error parsing content: {e}")
        return []

def open_url_in_browser(url):
    """
    Open a URL in the default browser on macOS.
    
    Args:
        url (str): The URL to open
    """
    try:
        subprocess.run(['open', url], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error opening URL {url}: {e}")
        return False
    except FileNotFoundError:
        print("Error: 'open' command not found. This script is designed for macOS.")
        return False

def main():
    """Main function to orchestrate the scraping and opening of stories."""
    print("🦞 Lobste.rs Story Opener")
    print("=" * 40)
    
    # Get stories from lobste.rs
    print("Fetching stories from lobste.rs...")
    stories = get_lobsters_stories()
    
    if not stories:
        print("No stories found or error occurred while fetching.")
        sys.exit(1)
    
    print(f"Found {len(stories)} stories!")
    print()
    
    # Ask user for confirmation
    print("Stories to open:")
    for i, story in enumerate(stories, 1):
        print(f"{i:2d}. {story['title']}")
    
    print()
    response = input(f"Open all {len(stories)} stories in your browser? (y/N): ").strip().lower()
    
    if response not in ['y', 'yes']:
        print("Cancelled.")
        sys.exit(0)
    
    # Open each story with a small delay
    print("\nOpening stories...")
    successful = 0
    
    for i, story in enumerate(stories, 1):
        print(f"Opening {i}/{len(stories)}: {story['title'][:60]}...")
        
        if open_url_in_browser(story['url']):
            successful += 1
            # Small delay to avoid overwhelming the browser
            time.sleep(0.5)
        else:
            print(f"Failed to open: {story['title']}")
    
    print(f"\n✅ Successfully opened {successful}/{len(stories)} stories!")

if __name__ == "__main__":
    main()