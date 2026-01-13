# AutoEmailChecker 📧

A program that checks and categorizes emails by connecting to your Gmail account. The final result will be saved as a CSV file. 

This program provides two approaches. One uses Anthorpic API key, which will cost little money ($5 to begin and about $0.003 for each email processed). The other approach uses a local AI model, Ollama, which is free but slower than using an API key. This program involves Python, Gmail API, and Anthropic API key. 

# 1. AutoEmailChecker with Anthropic API Key

## Requirement 
- Python 3.7+
- a Gmail account
- An Anthropic API key (for Claude)

## Installation & Setup

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
5. Download the credentials as `credentials.json` under `\claude` directory. 

**Step 4:** Create a .env file

```
ANTHROPIC_API_KEY=your_api_key_here
```

## Running

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

# 2. AutoEmailChecker with Ollama

## Requirement

- Python 3.7+
- A Gmail account
- 8GB RAM minimum
- 5-10GB free disk space for models

**Optional:**

- 16GB RAM recommended
- GPU (speed up the program)

## Installation & Setup

**Step 1:** Install Ollama

**Step 2:** Doanload an AI model
```
# Recommended: Llama 3.2 (2GB)
ollama pull llama3.2

# Alternative options:
ollama pull llama3.1 (~4.7GB)
ollama pull mistral (~4.1 GB)
ollama pull phi3 (~2.3GB)
```

**Step 3:** Install Python libraries

```
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client requests
```

**Step 4:** Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download the credentials as `credentials.json` under `\ollama` directory. 
## Running

**Step 1:** Start Ollama

The Ollama app should start automatically after installation. If not, start it manually. 

- Mac: Open Ollama from Applications
- Windows: Open Ollama from the Start Menu
- Linux:
```
ollama serve

# Verify if Ollama is running (should return a list of models):
ollama list
```

**Step 2:** Run Script
```
python email_categorizer.py
```

**Step 3:** Choose model

Example selection:
```
Which Ollama model do you want to use?
Recommended: llama3.2 (fast and good for email)
Enter model name: llama3.2
```

## Estimated Performance

Without GPU:
- 1st email: 5~10 seconds
- Subsequent emails: 2~5 seconds each

With GPU:
- 1~3 seconds each
