# SoftwareLicense.fyi 📋

> An AI-powered, community-maintained directory of software licensing rules — updated automatically every week via GitHub Actions.

## Live Site

🌐 **[View on GitHub Pages](https://navneet-20.github.io/SoftwareLicense.fyi/)**

---

## What It Does

This project automatically tracks whether popular software tools are:

| Category | Meaning |
|---|---|
| 🟢 **Open Source** | Source available, free for all use (MIT, GPL, Apache, etc.) |
| 🟣 **Free for Home** | Free for personal use only — commercial use requires payment |
| 🔴 **License Required** | A paid license is required for any use |
| 🟠 **License for Commercial** | Free personally, but paid for business use |
| 🔵 **Community Version** | Free community edition exists alongside paid tiers |

A Python script queries an AI model weekly to verify licensing status and auto-commits updated data back to the repo.

---

## Project Structure

```
/
├── data/
│   └── software_list.csv       # The main data source (auto-updated by CI)
├── public/
│   └── index.html              # The frontend (served by GitHub Pages)
├── scripts/
│   ├── update_licenses.py      # AI-powered license checker
│   └── requirements.txt        # Python dependencies
├── .github/
│   └── workflows/
│       └── update_data.yml     # GitHub Actions automation
└── README.md
```

---

## Setup Guide

### 1. Fork & Clone

```bash
git clone https://github.com/your-username/software-license-directory.git
cd software-license-directory
```

### 2. Enable GitHub Pages

In your repository → **Settings → Pages → Source**: set to `Deploy from branch`, branch `main`, folder `/public`.

### 3. Add API Secrets

In your repository → **Settings → Secrets and variables → Actions**, add:

| Secret Name | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key (if using GPT) |
| `GEMINI_API_KEY` | Your Google Gemini API key (if using Gemini) |
| `ANTHROPIC_API_KEY` | Your Anthropic API key (if using Claude) |

Only add the key for the provider you plan to use.

### 4. Choose Your AI Provider

Edit `.github/workflows/update_data.yml` and set the default provider:

```yaml
default: "openai"   # or "gemini" or "anthropic"
```

### 5. Run Locally (optional)

```bash
# Install Python dependencies
pip install -r scripts/requirements.txt

# Set your API key
export OPENAI_API_KEY="sk-..."
export AI_PROVIDER="openai"

# Run the updater
python scripts/update_licenses.py

# Serve the frontend locally
npx serve public/
```

---

## Adding New Software

To add software to the directory, edit `data/software_list.csv` and add a row:

```
My Software,Open Source,Free - Open Source,https://example.com/,2025-01-01,Brief licensing note
```

Columns:
- **Software Name** — The tool's common name
- **Category** — One of the 5 categories above
- **License Status** — Short human-readable status
- **Official URL** — Link to the official website or pricing page
- **Last Updated** — Date of last verification (YYYY-MM-DD)
- **Notes** — One sentence describing the key licensing detail

Submit a pull request and the AI will verify and update the entry on the next run.

---

## How the Automation Works

```
Every Monday 06:00 UTC
        ↓
GitHub Action triggers
        ↓
Python reads software_list.csv
        ↓
For each row:  AI prompt → JSON response → update row
        ↓
Updated CSV committed & pushed to main
        ↓
GitHub Pages serves the new data automatically
```

---

## Disclaimer

License data is AI-verified and updated weekly, but **always confirm licensing terms on the official vendor website** before using software commercially. This directory is for informational purposes only and does not constitute legal advice.

---

## Contributing

PRs welcome! You can:
- Add missing software (edit the CSV)
- Improve the frontend (`public/index.html`)
- Improve the AI prompt or script (`scripts/update_licenses.py`)
- Report outdated license data by opening an issue

---

## License

MIT — see [LICENSE](LICENSE)
