# JIRA Story Points Calculator

This script fetches JIRA issues from a given JIRA search URL and calculates the **total number of story points** assigned to those issues. It also identifies any issues that are missing story points.

## Features
- Extracts the JIRA instance and query from a **JIRA search URL**.
- Retrieves issue details using the **JIRA API**.
- Sums up the story points from all retrieved issues.
- Reports issues that do **not** have story points assigned.

---

## Prerequisites
Before using this script, ensure you have:
- **Python 3 installed** (check with `python --version` or `python3 --version`)
- A **JIRA API token** (see instructions below)

### Getting a JIRA API Token
1. Go to https://issues.redhat.com/secure/ViewProfile.jspa
2. Go to **Personal Access Tokens**.
3. Click **Create token**.
4. Copy and save the token securely.

---

## Installation
### 1. Clone or Download the Script
```sh
git clone https://github.com/your-repo/jira-story-points.git
cd jira-story-points
```
If you downloaded the script as a `.py` file, place it in a convenient folder.

### 2. Install Dependencies
The script uses the `requests` library to interact with JIRA's API. Install it with:
```sh
pip install requests
```

---

## Usage
Run the script with the **JIRA search URL** and your **API token**:

```sh
python story.py "<JIRA_SEARCH_URL>" -t <YOUR_API_TOKEN>
```

### Example
```sh
python story.py "https://issues.redhat.com/issues/?jql=project%20in%20(SRVCOM,%20SRVKE,%20SRVKS,%20SRVCLI,%20SRVOCF,%20SRVLOGIC)%20AND%20fixVersion%20%3D%201.36.0%20AND%20component%20%3D%20Documentation%20AND%20priority%20%3D%20Blocker%20ORDER%20BY%20priority%20DESC" -t my_api_token_here
```

### Example Output
```
Total Story Points: 42
Issues without story points:
- SRVCOM-1234
- SRVKE-5678
```

---

## Troubleshooting
- **Zsh: No matches found error?** Wrap the URL in quotes:
  ```sh
  python story.py "<JIRA_SEARCH_URL>" -t <YOUR_API_TOKEN>
  ```
- **ModuleNotFoundError: No module named 'requests'?** Install `requests`:
  ```sh
  pip install requests
  ```
- **400 Bad Request error?** Check that your **JIRA API token** is valid and that the **JQL query** in the URL is correct.

---

## Automating Execution (Optional)
You can create an alias in your `~/.zshrc` (Zsh) or `~/.bashrc` (Bash) file for easier usage:
```sh
echo 'alias jira_points="python /path/to/story.py -t YOUR_API_TOKEN"' >> ~/.zshrc
source ~/.zshrc
```
Now, simply run:
```sh
jira_points "<JIRA_SEARCH_URL>"
```

---


