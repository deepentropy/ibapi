#!/usr/bin/env python3
"""
Helper script to fetch the IB API download URL from the website
This script should be run on a machine with unrestricted web access
"""
import re
import sys

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed")
    print("Please run: pip install requests beautifulsoup4")
    sys.exit(1)


def fetch_download_url():
    """Fetch the download URL from the IB GitHub page"""
    url = "https://interactivebrokers.github.io/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print(f"Fetching {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        print("\nAlternative method:")
        print("1. Open https://interactivebrokers.github.io/ in your browser")
        print("2. Find the download link in the third row of the table")
        print("3. Right-click and copy the link address")
        print("4. Use that URL with update_ibapi.py")
        sys.exit(1)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Method 1: Find rows with class 'linebottom'
    rows = soup.find_all('tr', class_='linebottom')

    target_row = None
    if len(rows) >= 3:
        # Get the third linebottom row
        target_row = rows[2]
        print(f"Found {len(rows)} rows with class 'linebottom'")
    else:
        # Method 2: Look for any row containing a zip link
        print("Trying alternative method to find download link...")
        all_rows = soup.find_all('tr')
        for row in all_rows:
            link = row.find('a', href=re.compile(r'twsapi.*\.zip$'))
            if link:
                target_row = row
                break

    if not target_row:
        print("Could not find the target row with download link")
        print("\nFound links:")
        all_links = soup.find_all('a', href=re.compile(r'\.zip$'))
        for link in all_links:
            print(f"  {link.get('href')} - {link.text}")
        sys.exit(1)

    # Find the link in the row
    link = target_row.find('a', href=True)

    if not link:
        print("Could not find download link in the target row")
        sys.exit(1)

    download_url = link['href']

    # Make sure it's an absolute URL
    if not download_url.startswith('http'):
        base_url = 'https://interactivebrokers.github.io'
        download_url = base_url + ('/' if not download_url.startswith('/') else '') + download_url

    filename = download_url.split('/')[-1]

    print(f"\nSuccess!")
    print(f"  Download URL: {download_url}")
    print(f"  Filename: {filename}")

    # Extract version
    match = re.search(r'\.(\d+\.\d+)\.zip$', filename)
    if match:
        version = match.group(1)
        print(f"  Version: {version}")

    print(f"\nTo update the IB API, run:")
    print(f"  python update_ibapi.py {download_url}")

    return download_url


if __name__ == "__main__":
    fetch_download_url()
