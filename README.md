# AutoEmailChecker 📧
This program checks and categorizes emails in Gmail. 

## Requirement
- Python 3.7+
* a Gmail account
+ An Anthropic API key (for Claude)

## Setup Instruction 
**Step 1:** Install required libraries
```
pip install anthropic google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```

**Step 2:** Get your Anthropic API key
1. Go to console.anthropic.com
2. Sign up or log in
3. Go to API Keys section
4. Create a new key and copy it

**Step 3:** Enable Gmail API
1. Go to Google Cloud COnsole
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download the credentials as `credentials.json`

**Step 4:** Create a .env file
```
ANTHROPIC_API_KEY=your_api_key_here
```
## Running Instruction
