#!/usr/bin/env python3
"""
Helper script to fetch the IB API download URLs from the website
This script should be run on a machine with unrestricted web access
"""
import json
import re
import sys

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed")
    print("Please run: pip install requests beautifulsoup4")
    sys.exit(1)


def parse_raw_version(raw_version):
    """Convert IB raw version like '1050.02' into '10.50.02' (keeping the leading zero)"""
    match = re.fullmatch(r'(\d{2})(\d{2})\.(\d{2})', raw_version)
    if not match:
        raise ValueError(f"Unexpected version format: {raw_version}")
    major, minor, micro = match.groups()
    return f"{int(major)}.{int(minor)}.{micro}"


def extract_download_info():
    """Extract the Stable and Latest Linux installers with their metadata from the IB download page

    The page has one 'download-section-header' per channel (Stable, Latest) holding the version
    and release date, followed by a 'platform-grid' with one installer link per platform.
    The installer URLs are fixed per channel, so the version only comes from the header.
    """
    url = "https://download2.interactivebrokers.com/installers/tws-api/index.html"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print(f"Fetching {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, 'html.parser')

    downloads = []

    for header in soup.find_all('div', class_='download-section-header'):
        title = header.find('h2')
        meta = header.find(class_='section-meta')
        if not title or not meta:
            continue

        channel = title.get_text(strip=True).lower()
        meta_text = meta.get_text(' ', strip=True)

        version_match = re.search(r'Version:\s*(\d{4}\.\d{2})', meta_text)
        if not version_match:
            continue
        version = parse_raw_version(version_match.group(1))

        date_match = re.search(r'Release Date:\s*([A-Za-z]+\s+\d+\s+\d{4})', meta_text)
        release_date = date_match.group(1) if date_match else None

        release_notes_link = meta.find('a', href=re.compile(r'releasenotes'))
        release_notes_url = release_notes_link['href'] if release_notes_link else None

        # The Linux installer is a self-extracting install4j script that includes the Python source
        grid = header.find_next_sibling('div', class_='platform-grid')
        link = grid.find('a', href=re.compile(r'linux-x64\.sh$')) if grid else None
        if not link:
            continue

        downloads.append({
            'channel': channel,
            'url': link['href'],
            'version': version,
            'release_date': release_date,
            'platform': 'Linux',
            'release_notes': release_notes_url
        })

    if not downloads:
        print("Could not find any download links")
        sys.exit(1)

    return downloads


def get_channel_download(downloads, channel):
    """Return the download for a channel ('stable' or 'latest'), or None"""
    return next((d for d in downloads if d['channel'] == channel), None)


def display_downloads(downloads):
    """Display the download information in a readable format"""
    print(f"\nFound {len(downloads)} download(s):\n")

    for i, dl in enumerate(downloads, 1):
        print(f"{i}. Channel: {dl['channel']}")
        print(f"   Platform: {dl['platform']}")
        print(f"   Version: {dl['version']}")
        print(f"   Release Date: {dl['release_date']}")
        print(f"   Download URL: {dl['url']}")
        if dl['release_notes']:
            print(f"   Release Notes: {dl['release_notes']}")
        print()

    # Also save to JSON file
    output_file = 'download_info.json'
    with open(output_file, 'w') as f:
        json.dump(downloads, f, indent=2)
    print(f"Download information saved to {output_file}")

    # Show example usage
    latest = get_channel_download(downloads, 'latest')
    if latest:
        print(f"\nTo update to the latest version, run:")
        print(f"  python update_ibapi.py {latest['url']} latest {latest['version']}")


if __name__ == "__main__":
    downloads = extract_download_info()
    display_downloads(downloads)
