# IsItFree?

**IsItFree?** is a software licensing discovery and reference website that helps users quickly understand whether software is free, open source, freemium, subscription-based, or paid.

🌐 **Website:** https://isitfree.webline.cloud/
👤 **Portfolio:** https://navneet.webline.cloud/

---

## 🚀 Latest Update

### Increased Daily Software Discovery

The automated software discovery system has been upgraded from:

**10 new software entries per run → 20 new software entries per run**

The discovery limit is controlled by:

```python
NEW_PER_RUN = 20
```

in:

```text
scripts/discover_software.py
```

The daily GitHub Action automatically runs the discovery process and adds newly discovered software to the project database.

---

## 🤖 AI-Powered Software Updates

The project uses an automated AI-assisted workflow to discover and maintain software information.

The system can discover software and collect information such as:

* Software name
* Category
* License type
* Official website
* Description
* Source/repository information
* Pricing information when available
* Software availability

The website displays the latest AI update information based on the software database.

---

## 📊 Software Database

Software information is stored in:

```text
data/software_list.csv
```

The website dynamically reads the database so that software counts and update information remain synchronized with the CSV.

### Important

Do not hardcode the number of software entries in `index.html`.

The website should calculate the total directly from the CSV.

For example:

```text
150 software entries
```

will automatically become:

```text
151 software entries
```

when another valid entry is added.

---

## 🔄 Automated Discovery

The daily discovery workflow is located at:

```text
.github/workflows/discover_daily.yml
```

The workflow runs the discovery script:

```text
scripts/discover_software.py
```

The current configuration allows:

```python
NEW_PER_RUN = 20
```

new software entries per run.

---

## 🖥️ Website Features

### Software Search

Users can search the software directory directly from the homepage.

The `/` keyboard shortcut can be used to quickly focus/open the search interface.

### Categories

Software is organized into categories.

Selecting a category opens the directory with the appropriate category filter applied.

### License Information

Each software entry displays its available licensing information, making it easier to determine whether the software is:

* Free
* Open Source
* Freemium
* Commercial
* Subscription-based
* Trial
* Other licensing models

### Last AI Update

The website displays when the software information was most recently updated.

This information is derived from the project data rather than relying on a manually entered software count.

---

## ⚑ Report an Error

Users can report incorrect software information directly from the directory.

The **Flag Error** option allows users to submit information such as:

* Incorrect license
* Incorrect website
* Incorrect category
* Outdated information
* Incorrect description
* Other errors

This helps keep the software database accurate.

---

## 💡 Suggest Software

Users can also suggest software that is missing from the directory.

Suggestions can be submitted through the website and reviewed before being added to the database.

---

## 🚧 Upcoming Features

The following features are planned for future releases.

### 1. Compare Options

Allow users to compare multiple software products side-by-side.

Potential comparison fields:

* License
* Features
* Platform
* Pricing
* Open-source status
* Pros and cons

### 2. Approximate Pricing

Add estimated pricing information for commercial software.

Possible information:

* Free tier
* Starting price
* Monthly pricing
* Annual pricing
* Business pricing
* Enterprise pricing

Pricing will be presented as approximate information and users should verify the current price with the software vendor.

### 3. Free Alternatives

Show free and open-source alternatives to commercial software.

For example:

```text
Microsoft Office
        ↓
LibreOffice
        ↓
ONLYOFFICE
```

This will help users discover lower-cost or free alternatives.

---

## 📁 Project Structure

```text
SoftwareLicense.fyi/
│
├── data/
│   └── software_list.csv
│
├── scripts/
│   └── discover_software.py
│
├── .github/
│   └── workflows/
│       └── discover_daily.yml
│
├── index.html
└── README.md
```

---

## ⚙️ Updating the Daily Limit

To change the number of software entries discovered per run, edit:

```text
scripts/discover_software.py
```

Find:

```python
NEW_PER_RUN = 20
```

For example, to process 30 entries:

```python
NEW_PER_RUN = 30
```

The GitHub Action should continue using the same discovery script.

---

## ⚠️ Important Development Rule

The website frontend and automated backend are separate components.

When making frontend design changes:

* Do not modify Python discovery logic unnecessarily.
* Do not modify the CSV structure without updating dependent code.
* Do not hardcode software counts.
* Keep software counts dynamically calculated from `data/software_list.csv`.
* Preserve the existing automated GitHub workflow.

---

## 🌐 Project

**IsItFree?**

A simple way to discover software and understand its licensing.

Website: https://isitfree.webline.cloud/

Portfolio: https://navneet.webline.cloud/

---

## 📌 Current Release

### Version Update

**Daily discovery:** 20 new software entries per run
**Database:** CSV-based
**Discovery:** Automated
**Updates:** AI-assisted
**Search:** Enabled
**Categories:** Enabled
**Error reporting:** Enabled
**Software suggestions:** Enabled

### Planned

* Software comparison
* Approximate pricing
* Free alternatives
* More detailed software information
* Improved licensing intelligence
* Continued automated database expansion
