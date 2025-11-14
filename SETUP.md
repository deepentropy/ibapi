# Setup Guide for IB API Automation

This guide will help you complete the setup and perform the first IB API update.

## Current Status

✅ Automation scripts created
✅ GitHub Actions workflow configured
✅ README and documentation added
⏳ Waiting for first IB API download and commit

## Prerequisites

1. Python 3.7+ installed
2. Required packages:
   ```bash
   pip install requests beautifulsoup4
   ```

## Step-by-Step Setup

### Option 1: Automatic Download (Recommended)

If you have unrestricted web access, you can use the automation scripts:

```bash
# Step 1: Get the download URL from IB website
python get_download_url.py

# Step 2: Use the URL to download and commit the API
python update_ibapi.py <url_from_step_1>
```

The script will:
- Download the TWS API zip file
- Extract the Python client (`IBJts/source/pythonclient`)
- Copy it to the `ibapi/` directory
- Commit the changes
- Create a version tag

### Option 2: Manual Download

If automatic download fails due to network restrictions:

1. **Get the Download URL manually:**
   - Open https://interactivebrokers.github.io/ in your browser
   - Look for the downloads table on the page
   - Find the third row (usually has class `linebottom`)
   - Right-click on the download link in the second column
   - Copy link address

   The link should look like:
   ```
   https://interactivebrokers.github.io/downloads/twsapi_macunix.1040.01.zip
   ```

2. **Run the automation script:**
   ```bash
   python update_ibapi.py https://interactivebrokers.github.io/downloads/twsapi_macunix.XXXX.XX.zip
   ```

   Replace `XXXX.XX` with the actual version number from the URL you copied.

3. **Verify the commit:**
   ```bash
   git log --oneline -5
   git tag -l
   ```

   You should see:
   - A commit message: "Update IB API to version XXXX.XX"
   - A tag: "vXXXX.XX"

4. **Push to remote (if not already pushed):**
   ```bash
   git push origin claude/scrape-ib-api-publish-01CNiDPtbK2whUmxaWrsLJtm --tags
   ```

### Option 3: Completely Manual Process

If you prefer full control:

1. Download the TWS API zip from https://interactivebrokers.github.io/
2. Extract the zip file
3. Locate the `IBJts/source/pythonclient` directory
4. Copy all files to this repository's `ibapi/` directory:
   ```bash
   mkdir -p ibapi
   cp -r /path/to/extracted/IBJts/source/pythonclient/* ibapi/
   ```
5. Commit and tag:
   ```bash
   git add ibapi/
   git commit -m "Update IB API to version X.XX"
   git tag -a vX.XX -m "Version X.XX"
   git push origin claude/scrape-ib-api-publish-01CNiDPtbK2whUmxaWrsLJtm --tags
   ```

## GitHub Actions Automation

The GitHub Actions workflow (`.github/workflows/update-ibapi.yml`) is configured to:

- Run weekly on Mondays at 9 AM UTC
- Can be triggered manually from the Actions tab
- Automatically checks for updates
- Commits and tags new versions
- Creates GitHub releases

To manually trigger:
1. Go to the Actions tab in GitHub
2. Select "Update IB API" workflow
3. Click "Run workflow"

## Troubleshooting

### Network/Proxy Issues

If you're behind a corporate proxy or firewall:

1. The automation scripts may fail with 403 errors
2. Use Option 2 or 3 above (manual download)
3. Or run the scripts from a different network environment

### SSL Certificate Errors

If you see SSL/certificate errors:

1. The scripts disable SSL verification by default
2. If still failing, try manual download from browser

### Version Extraction Fails

The script expects filenames like: `twsapi_macunix.1040.01.zip`

If your filename is different:
1. Check the filename format
2. Modify the regex in `extract_version_from_filename()` in `update_ibapi.py`

## Next Steps

After the first successful update:

1. **Verify the commit:**
   ```bash
   ls -la ibapi/
   git log
   git tag
   ```

2. **Test the Python client:**
   ```bash
   python -c "import sys; sys.path.insert(0, 'ibapi'); from ibapi.client import EClient; print('Import successful!')"
   ```

3. **Set up PyPI publishing** (future enhancement):
   - Create `setup.py`
   - Configure PyPI credentials
   - Add publishing step to GitHub Actions

4. **Enable automatic updates:**
   - The GitHub Actions workflow will now run weekly
   - It will check for new versions and update automatically

## Support

- IB API issues: Contact Interactive Brokers
- Automation script issues: Check the GitHub repository issues
- For questions about this setup: Review the README.md

## File Structure After First Update

```
ibapi-python/
├── .github/
│   └── workflows/
│       └── update-ibapi.yml     # GitHub Actions workflow
├── ibapi/                        # IB Python client (added after first run)
│   ├── __init__.py
│   ├── client.py
│   ├── wrapper.py
│   ├── contract.py
│   └── ... (other API files)
├── README.md                     # Main documentation
├── SETUP.md                      # This file
├── update_ibapi.py               # Main automation script
├── get_download_url.py           # URL fetcher
├── find_latest_version.py        # Version finder
└── scrape_and_publish.py         # Alternative script
```

## Testing the Setup

To test without actually downloading:

```python
# Test version extraction
python -c "
from update_ibapi import extract_version_from_filename
print(extract_version_from_filename('twsapi_macunix.1040.01.zip'))
# Should output: 1040.01
"
```

---

**Ready to proceed?** Follow Option 1 or 2 above to complete your first IB API update!
