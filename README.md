# ibapi-python

Automated publisher for the Interactive Brokers TWS API Python client on PyPI.

[![PyPI version](https://badge.fury.io/py/ibapi-python.svg)](https://pypi.org/project/ibapi-python/)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-IB%20API-blue.svg)](https://interactivebrokers.github.io/tws-api)

## 📦 Installation

```bash
pip install ibapi-python
```

## 🚀 Usage

```python
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

class IBApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

app = IBApp()
app.connect("127.0.0.1", 7497, clientId=1)
app.run()
```

For complete examples and documentation, visit the [official IB API documentation](https://ibkrcampus.com/ibkr-api-page/).

## 📋 About This Package

This is an automated publisher for the Interactive Brokers TWS API Python client. The source code is from Interactive Brokers' official TWS API distribution, packaged and published to PyPI for easy installation.

### Two Versions Available

- **Latest**: The newest IB API version (published on `main` branch)
- **Stable**: Previous IB API versions (published on `stable` branch)

All versions are automatically published to PyPI weekly.

## 🏗️ Project Structure

```
ibapi-python/
├── .github/
│   └── workflows/           # GitHub Actions for automation
│       ├── update-ibapi-latest.yml   # Latest version publisher
│       └── update-ibapi-stable.yml   # Stable version publisher
├── scripts/                 # Automation scripts
│   ├── get_download_url.py  # Fetch IB API download URLs
│   ├── update_ibapi.py      # Download and commit IB API
│   └── check_and_update.py  # Orchestrator (legacy)
├── ibapi/                   # IB API Python client (auto-updated)
│   └── ibapi/
│       ├── client.py
│       ├── wrapper.py
│       └── ...
├── pyproject.toml           # Package configuration
└── README.md
```

## 🔄 How It Works

### Automated Workflow

1. **Weekly Check**: GitHub Actions runs every Monday at 9:00 AM UTC
2. **Version Detection**: Scrapes https://interactivebrokers.github.io/ for new versions
3. **Download & Extract**: Downloads the TWS API zip and extracts the Python client
4. **Auto-Fix**: Automatically fixes version strings and package configuration
5. **Build & Publish**: Builds the package and publishes to PyPI
6. **Tag & Release**: Creates git tags and GitHub releases

### Version Management

- Versions follow IB's format: `10.40.01`, `10.37.02`, etc.
- Git tags: `v10.40.01`, `v10.37.02`, etc.
- Package names: `ibapi-python==10.40.01`, `ibapi-python==10.37.02`, etc.

## 🛠️ Development

### Prerequisites

```bash
pip install requests beautifulsoup4 build
```

### Manual Update

```bash
# Get download URL
python scripts/get_download_url.py

# Update to specific version
python scripts/update_ibapi.py https://interactivebrokers.github.io/downloads/twsapi_macunix.1040.01.zip
```

### Scripts

- **`scripts/get_download_url.py`**: Scrapes IB website for download URLs
- **`scripts/update_ibapi.py`**: Downloads, extracts, fixes, and commits IB API
  - Fixes version in `ibapi/__init__.py` (preserves leading zeros)
  - Fixes `pyproject.toml` (removes setuptools_scm, deprecated license)
  - Cleans `__pycache__` directories
- **`scripts/check_and_update.py`**: Legacy orchestrator (not used by workflows)

## 📝 License

The Interactive Brokers TWS API is proprietary software owned by Interactive Brokers LLC. This package is an automated publisher that makes the official IB API Python client available on PyPI for convenience.

- IB API License: [IB API Non-Commercial License or IB API Commercial License](https://interactivebrokers.github.io/tws-api)
- This automation tool: MIT License

## 🔗 Links

- **PyPI Package**: https://pypi.org/project/ibapi-python/
- **Official IB API**: https://interactivebrokers.github.io/tws-api
- **Documentation**: https://ibkrcampus.com/ibkr-api-page/
- **GitHub Repository**: https://github.com/yourusername/ibapi-python

## 🐛 Support

For issues with:
- **The IB API itself**: Contact [Interactive Brokers](https://www.interactivebrokers.com/en/support/contact.php)
- **This package/automation**: Open an [issue on GitHub](https://github.com/yourusername/ibapi-python/issues)

## ⚙️ Configuration

The package configuration is in `pyproject.toml`:

```toml
[project]
name = "ibapi-python"
dynamic = ["version"]  # Version from ibapi.__version__
dependencies = ["protobuf==5.29.3"]

[tool.setuptools]
packages = ["ibapi", "ibapi.protobuf"]
package-dir = {"" = "ibapi"}  # Maps ibapi/ibapi/* to ibapi/*
```

This ensures imports work as expected:
```python
from ibapi.client import EClient  # Not from ibapi.ibapi.client
```
