import os
import base64
import csv
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']  # Changed from readonly to modify

class EmailCategorizer:
    def __init__(self):
        self.gmail_service = None
        self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
    def authenticate_gmail(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # Check if token.json exists (stores user's access tokens)
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        self.gmail_service = build('gmail', 'v1', credentials=creds)
        print("✓ Gmail authenticated successfully!")
    
    def fetch_emails(self, max_results=20):
        """Fetch recent emails from Gmail"""
        print(f"\nFetching {max_results} recent emails...")
        
        results = self.gmail_service.users().messages().list(
            userId='me', 
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        emails = []
        for msg in messages:
            # Get full message details
            message = self.gmail_service.users().messages().get(
                userId='me', 
                id=msg['id'],
                format='full'
            ).execute()
            
            # Extract email data
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
            
            # Get email body
            body = self.get_email_body(message['payload'])
            
            emails.append({
                'id': msg['id'],
                'subject': subject,
                'from': sender,
                'date': date,
                'body': body[:1000]  # Limit body length for API
            })
        
        print(f"✓ Fetched {len(emails)} emails")
        return emails
    
    def get_email_body(self, payload):
        """Extract email body from payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
                        break
        else:
            data = payload['body'].get('data', '')
            if data:
                body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        return body
    
    def categorize_email(self, email):
        """Use Claude to categorize a single email"""
        prompt = f"""Analyze this email and categorize it. """

Subject: {email['subject']}
From: {email['from']}
Body: {email['body']}

Provide your analysis in this exact format:
CATEGORY: [Choose ONE: ACTION_REQUIRED, INFORMATIONAL, PROMOTIONAL, SPAM, SOCIAL, SUSPICIOUS, NEEDS_REVIEW]
PRIORITY: [Choose ONE: HIGH, MEDIUM, LOW]
ACTION_ITEMS: [List specific actions needed, or write "None"]
SUMMARY: [One sentence summary]
SCAM_INDICATORS: [List any red flags, or write "None"]
CONFIDENCE: [Choose ONE: HIGH, MEDIUM, LOW]

Guidelines:
- ACTION_REQUIRED: Needs a response or action (interviews, meetings, deadlines, approvals)
- INFORMATIONAL: FYI emails, newsletters, updates
- PROMOTIONAL: Marketing, sales, advertisements
- SPAM: Unwanted or suspicious emails
- SOCIAL: Social media notifications, personal messages
- SUSPICIOUS: Contains scam indicators like phishing attempts, fake urgency, suspicious links, impersonation, or requests for sensitive info
- NEEDS_REVIEW: You're uncertain about the email's intent or legitimacy

Priority:
- HIGH: Urgent deadlines, interview scheduling, important decisions, OR suspicious emails needing immediate attention
- MEDIUM: Non-urgent responses needed
- LOW: Can be handled later or archived

Scam Indicators to Look For:
- Urgency tactics ("Your account will be closed!", "Act now!", "Verify within 24 hours")
- Requests for passwords, SSN, credit card info, or other sensitive data
- Suspicious sender email (mismatched domain, typos in company name)
- Generic greetings ("Dear Customer" instead of your name)
- Poor grammar or spelling
- Threats or fear-inducing language
- Too-good-to-be-true offers
- Unexpected attachments or links
- Impersonation of known companies/people
- Mismatched or shortened URLs

Confidence:
- HIGH: Clear and certain about the categorization
- MEDIUM: Fairly confident but some ambiguity
- LOW: Uncertain, needs human review

        try:
            message = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response = message.content[0].text
            
            # Parse response
            category = "UNKNOWN"
            priority = "LOW"
            action_items = "None"
            summary = ""
            
            for line in response.split('\n'):
                if line.startswith('CATEGORY:'):
                    category = line.replace('CATEGORY:', '').strip()
                elif line.startswith('PRIORITY:'):
                    priority = line.replace('PRIORITY:', '').strip()
                elif line.startswith('ACTION_ITEMS:'):
                    action_items = line.replace('ACTION_ITEMS:', '').strip()
                elif line.startswith('SUMMARY:'):
                    summary = line.replace('SUMMARY:', '').strip()
            
            return {
                'category': category,
                'priority': priority,
                'action_items': action_items,
                'summary': summary
            }
            
        except Exception as e:
            print(f"Error categorizing email: {e}")
            return {
                'category': 'ERROR',
                'priority': 'LOW',
                'action_items': 'None',
                'summary': f'Error: {str(e)}',
                'scam_indicators': 'None',
                'confidence': 'LOW'
            }
    
    def process_emails(self, max_emails=20):
        """Process and categorize all emails"""
        self.authenticate_gmail()
        emails = self.fetch_emails(max_emails)
        
        categorized_emails = []
        
        print("\nCategorizing emails with Claude AI...")
        for i, email in enumerate(emails, 1):
            print(f"Processing {i}/{len(emails)}: {email['subject'][:50]}...")
            
            analysis = self.categorize_email(email)
            
            categorized_emails.append({
                'id': email['id'],
                'subject': email['subject'],
                'from': email['from'],
                'date': email['date'],
                'category': analysis['category'],
                'priority': analysis['priority'],
                'action_items': analysis['action_items'],
                'summary': analysis['summary'],
                'scam_indicators': analysis['scam_indicators'],
                'confidence': analysis['confidence'],
                'is_unread': email['is_unread']
            })
        
        return categorized_emails
    
    def save_to_csv(self, categorized_emails, filename='categorized_emails.csv'):
        """Save results to CSV file"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'subject', 'from', 'date', 'category', 
                'priority', 'action_items', 'summary'
            ])
            writer.writeheader()
            writer.writerows(categorized_emails)
        
        print(f"\n✓ Results saved to {filename}")

def main():
    categorizer = EmailCategorizer()
    
    # Process 20 most recent emails
    results = categorizer.process_emails(max_emails=20)
    
    # Save to CSV
    categorizer.save_to_csv(results)
    
    # Print summary
    print("\n" + "="*60)
    print("CATEGORIZATION SUMMARY")
    print("="*60)
    
    # Count by category
    categories = {}
    action_required = []
    
    for email in results:
        cat = email['category']
        categories[cat] = categories.get(cat, 0) + 1
        
        if email['category'] == 'ACTION_REQUIRED':
            action_required.append(email)
    
    print("\nBy Category:")
    for cat, count in categories.items():
        print(f"  {cat}: {count}")
    
    print(f"\n🔔 ACTION REQUIRED EMAILS ({len(action_required)}):")
    for email in action_required:
        print(f"\n  Subject: {email['subject']}")
        print(f"  Priority: {email['priority']}")
        print(f"  Action: {email['action_items']}")

if __name__ == '__main__':
    main()
