# IB API Python - Automated Publisher

This project automatically downloads the Interactive Brokers TWS API Python client and publishes it to PyPI.

## Overview

The Interactive Brokers TWS API is distributed as a zip file containing multiple language bindings. This project:

1. Downloads the latest TWS API zip file from https://interactivebrokers.github.io/
2. Extracts only the Python client (`IBJts/source/pythonclient`)
3. Commits the extracted code to a git branch
4. Tags the commit with the API version number
5. (Future) Publishes to PyPI automatically

## Quick Start

### Method 1: Automatic (if web access is unrestricted)

```bash
# Get the download URL from the IB website
python get_download_url.py

# Update the IB API using the URL from above
python update_ibapi.py <download_url>
```

### Method 2: Manual URL

If automatic scraping doesn't work (e.g., due to firewall/proxy restrictions):

1. Open https://interactivebrokers.github.io/ in your browser
2. Find the download link in the table (usually the third row: `tr.linebottom:nth-child(3) > td:nth-child(2) > a`)
3. Right-click and copy the link address
4. Run the update script:

```bash
python update_ibapi.py <download_url>
```

Example:
```bash
python update_ibapi.py https://interactivebrokers.github.io/downloads/twsapi_macunix.1040.01.zip
```

## How It Works

### Version Detection

The version is automatically extracted from the zip filename. For example:
- `twsapi_macunix.1040.01.zip` → version `1040.01`
- `twsapi_macunix.1051.00.zip` → version `1051.00`

### Git Workflow

1. The Python client code is copied to the `ibapi/` directory
2. Changes are committed with message: `Update IB API to version X.XX`
3. A git tag is created: `vX.XX`

### File Structure

```
ibapi-python/
├── README.md                 # This file
├── get_download_url.py      # Helper script to fetch download URL
├── update_ibapi.py          # Main automation script
├── scrape_and_publish.py    # Legacy script (alternative method)
└── ibapi/                   # IB Python client code (created after first run)
    ├── client.py
    ├── wrapper.py
    └── ...
```

## Requirements

```bash
pip install requests beautifulsoup4
```

## Manual Steps (Alternative)

If you prefer to do it manually:

1. Download the TWS API zip from https://interactivebrokers.github.io/
2. Extract the zip file
3. Copy `IBJts/source/pythonclient/*` to `ibapi/` in this repository
4. Commit and tag:

```bash
git add ibapi/
git commit -m "Update IB API to version X.XX"
git tag -a vX.XX -m "Version X.XX"
```

## Future Enhancements

- [ ] Automatic publishing to PyPI
- [ ] GitHub Actions workflow for scheduled checks
- [ ] Version comparison to detect updates
- [ ] Automated testing of the Python client
- [ ] setup.py for PyPI packaging

## License

The IB API code is proprietary to Interactive Brokers. This automation tool is provided as-is.

## Support

For issues with:
- The IB API itself: Contact Interactive Brokers
- This automation tool: Open an issue in this repository
