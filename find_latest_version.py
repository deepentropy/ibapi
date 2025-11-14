#!/usr/bin/env python3
"""
Script to find the latest available IB API version by probing URLs
"""
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_url(url):
    """Check if a URL is accessible"""
    try:
        response = requests.head(url, verify=False, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except:
        return False


def find_latest():
    """Try to find the latest version by checking multiple URLs"""
    base_patterns = [
        "https://interactivebrokers.github.io/downloads/twsapi_macunix.{}.{:02d}.zip",
        "https://interactivebrokers.github.io/twsapi_macunix.{}.{:02d}.zip",
        "https://github.com/InteractiveBrokers/tws-api-public/releases/download/v{}.{:02d}/twsapi_macunix.{}.{:02d}.zip",
    ]

    # Try recent versions (starting from 1051 and going backwards)
    for major in range(1051, 1030, -1):
        for minor in range(1, 20):
            for pattern in base_patterns:
                try:
                    url = pattern.format(major, minor, major, minor) if pattern.count('{}') == 4 else pattern.format(major, minor)
                    print(f"Trying: {url}")

                    if check_url(url):
                        print(f"\n✓ FOUND: {url}")
                        return url
                except:
                    continue

    return None


if __name__ == "__main__":
    print("Searching for latest IB API version...")
    url = find_latest()

    if url:
        print(f"\nLatest version found: {url}")
        print(f"\nTo update, run:")
        print(f"  python update_ibapi.py {url}")
    else:
        print("\nNo accessible version found")
        print("Please manually check https://interactivebrokers.github.io/")
