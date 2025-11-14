#!/usr/bin/env python3
"""
Script to download Interactive Brokers TWS API and extract Python client
"""
import os
import re
import sys
import zipfile
import shutil
import requests
from pathlib import Path


def extract_version_from_filename(filename):
    """Extract version number from filename like twsapi_macunix.1040.01.zip"""
    match = re.search(r'\.(\d+\.\d+)\.zip$', filename)
    if match:
        return match.group(1)

    # Try alternative pattern
    match = re.search(r'twsapi.*?(\d+\.\d+)', filename)
    if match:
        return match.group(1)

    raise ValueError(f"Could not extract version from filename: {filename}")


def download_file(url, dest_path):
    """Download a file from URL to destination path"""
    print(f"Downloading {url}...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    response = requests.get(url, headers=headers, stream=True, verify=False)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    print(f"File size: {total_size / 1024 / 1024:.2f} MB")

    with open(dest_path, 'wb') as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                print(f"\rProgress: {percent:.1f}%", end='', flush=True)

    print(f"\nDownloaded to {dest_path}")


def extract_pythonclient(zip_path, extract_to='.'):
    """Extract the pythonclient directory from the zip file"""
    print(f"\nExtracting {zip_path}...")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # List all files to find the pythonclient directory
        all_files = zip_ref.namelist()

        # Find files in pythonclient path (case insensitive)
        pythonclient_files = [f for f in all_files if 'pythonclient' in f.lower()]

        if not pythonclient_files:
            print("Available files in zip:")
            for f in all_files[:30]:  # Print first 30 files
                print(f"  {f}")
            raise ValueError("Could not find pythonclient directory in zip file")

        # Find the base path for pythonclient
        # Look for pattern like IBJts/source/pythonclient
        base_path = None
        for file in pythonclient_files:
            if 'pythonclient' in file.lower():
                # Extract the path up to and including pythonclient
                parts = file.split('/')
                try:
                    pythonclient_idx = next(i for i, p in enumerate(parts) if 'pythonclient' in p.lower())
                    base_path = '/'.join(parts[:pythonclient_idx+1])
                    break
                except StopIteration:
                    continue

        if not base_path:
            raise ValueError("Could not determine pythonclient base path")

        print(f"Found pythonclient at: {base_path}")

        # Extract only pythonclient files
        extracted_files = []
        for file in all_files:
            if file.startswith(base_path) and not file.endswith('/'):
                zip_ref.extract(file, extract_to)
                extracted_files.append(file)

        print(f"Extracted {len(extracted_files)} files")

        return base_path


def main():
    """Main function to orchestrate the download and extraction"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Check if URL was provided as argument
    if len(sys.argv) > 1:
        download_url = sys.argv[1]
        filename = os.path.basename(download_url)
        print(f"Using provided URL: {download_url}")
    else:
        # Try to use a known recent version URL pattern
        # Based on research, the download URLs follow this pattern
        print("No URL provided. Please provide the download URL as an argument.")
        print("Usage: python scrape_and_publish.py <download_url>")
        print("\nExample:")
        print("  python scrape_and_publish.py https://interactivebrokers.github.io/downloads/twsapi_macunix.1040.01.zip")
        print("\nYou can find the latest version at: https://interactivebrokers.github.io/")
        sys.exit(1)

    try:
        # Extract version
        version = extract_version_from_filename(filename)
        print(f"Version: {version}")

        # Download the zip file
        zip_path = f"/tmp/{filename}"
        download_file(download_url, zip_path)

        # Extract pythonclient
        extracted_path = extract_pythonclient(zip_path, '/tmp')

        print(f"\nExtraction complete!")
        print(f"Version: {version}")
        print(f"Extracted path: {extracted_path}")
        print(f"Full path: /tmp/{extracted_path}")

        # Return the paths for further processing
        return version, f"/tmp/{extracted_path}"

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
