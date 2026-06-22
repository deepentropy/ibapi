# ibapi

Automated publisher for the Interactive Brokers TWS API Python client on PyPI.

[![PyPI Latest](https://img.shields.io/pypi/v/ibapi-latest?label=latest)](https://pypi.org/project/ibapi-latest/)
[![PyPI Stable](https://img.shields.io/pypi/v/ibapi-stable?label=stable)](https://pypi.org/project/ibapi-stable/)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-IB%20API%20Non--Commercial-blue.svg)](LICENSE)

## 📦 Installation

**Two packages available on PyPI:**

### Latest Version (Recommended)
```bash
pip install ibapi-latest
```

### Stable Version
```bash
pip install ibapi-stable
```

You can also install a specific version:
```bash
pip install ibapi-latest==10.40.01
pip install ibapi-stable==10.37.02
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

This is an **unofficial** automated publisher for the Interactive Brokers TWS API Python client. The source code is from Interactive Brokers' official TWS API distribution, packaged and published to PyPI for easy installation.

> **⚠️ DISCLAIMER**
>
> This package is **NOT officially affiliated with, endorsed by, or supported by Interactive Brokers LLC**. It is an independent community project that automates the packaging and distribution of the official IB API source code.
>
> - The IB API source code is proprietary to Interactive Brokers and is licensed under the [TWS API Non-Commercial License](LICENSE)
> - This automation tool is provided "as is" without any warranties
> - For official support, please contact [Interactive Brokers](https://www.interactivebrokers.com/en/support/contact.php)
> - Trading involves risk. Use at your own discretion.

### Two PyPI Packages

- **`ibapi-latest`**: The newest IB API version (from `main` branch)
- **`ibapi-stable`**: Previous IB API versions (from `stable` branch)

Both packages are automatically updated weekly when new IB API versions are released.

## 🏗️ Project Structure

```
ibapi/
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
- Git tags: `v10.47.01-latest` (latest channel), `v10.46.01-stable` (stable channel)
- PyPI packages:
  - Latest: `ibapi-latest==10.40.01`
  - Stable: `ibapi-stable==10.37.02`

## 📝 License

This project has a **dual license structure**:

### IB API Source Code (`ibapi/` directory)

The Interactive Brokers TWS API source code is proprietary software owned by Interactive Brokers LLC and is licensed under the **[TWS API Non-Commercial License](LICENSE)**.

**Key restrictions:**
- ✅ Use for personal trading and account management
- ✅ Develop internal proprietary tools for your own IB account
- ❌ **NOT permitted**: Selling software to third parties
- ❌ **NOT permitted**: Distributing software to generate indirect financial benefit (e.g., commissions)
- ⚠️ **Requires**: Active Interactive Brokers account

**For commercial use**, contact Interactive Brokers at: opensource@interactivebrokers.com

**Full license text**: See [LICENSE](LICENSE) file

### Automation Scripts (`scripts/` directory, workflows)

The automation tooling that packages and publishes the IB API is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for complete details.

## 🔗 Links

- **PyPI Packages**:
  - Latest: https://pypi.org/project/ibapi-latest/
  - Stable: https://pypi.org/project/ibapi-stable/
- **Official IB API**: https://interactivebrokers.github.io/tws-api
- **Documentation**: https://ibkrcampus.com/ibkr-api-page/
- **GitHub Repository**: https://github.com/yourusername/ibapi

## 🐛 Support

For issues with:
- **The IB API itself**: Contact [Interactive Brokers](https://www.interactivebrokers.com/en/support/contact.php)
- **This package/automation**: Open an [issue on GitHub](https://github.com/yourusername/ibapi/issues)

## ⚙️ Configuration

The package configuration is in `pyproject.toml`:

```toml
[project]
name = "ibapi"
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
