# AutoEmailChecker 📧
A program that checks and categorizes emails in your Gmail account. This program involves Python, Gmail API, and Anthropic API key. 

## Requirement
- Python 3.7+
- a Gmail account
- An Anthropic API key (for Claude)

## Setup Instruction

**Step 1:** Install required libraries
```
pip install anthropic google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```

**Step 2:** Get your Anthropic API key

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Go to the API Keys section
4. Create a new key and copy it

**Step 3:** Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download the credentials as `credentials.json` under `\checker` directory. 

**Step 4:** Create a .env file

```
ANTHROPIC_API_KEY=your_api_key_here
```

## Running Instruction

**Step 1:** file preparation

Make sure the following files are in the same folder:
- `email_categorizer.py` (from repository)
- `credentials.json` (from Google Cloud)
- `.env` (with your Anthropic API key)

**Step 2:** Run script

```
python email_categorizer.py
```

**Step 3:** First-time authentication

The first time you run it:

1. A browser window will open
2. Log in to your Gmail account
3. Grant the app permission to read your email
4. The script will create a `token.json` file

### Expected Output
> ============================================================ EMAIL CATEGORIZATION TOOL ============================================================ Choose what emails to categorize: 1. Recent emails (default 20) 2. Emails from a specific date range Enter your choice (1 or 2, press Enter for 1): 2 Enter date range (format: YYYY/MM/DD) Start date (e.g., 2025/07/01): 2025/07/01 End date (e.g., 2025/08/01): 2025/08/01 Maximum emails to process (default 100): 50 Which emails do you want to process? 1. All emails (both read and unread) 2. Only unread emails 3. Only already-read emails Enter your choice (1, 2, or 3, press Enter for 1): 2 ============================================================ PROCESSING CONFIGURATION ============================================================ Date Range: 2025/07/01 to 2025/08/01 Scope: Only unread emails Proceed with categorization? (Y/n): y ============================================================ CATEGORIZING EMAILS ============================================================ ✓ Gmail authenticated successfully! Fetching emails... ✓ Fetched 23 emails Categorizing 23 emails with Claude AI... Processing 1/23 📭: Interview Schedule Request... Processing 2/23 📬: Weekly Newsletter... ...

## Fixes
