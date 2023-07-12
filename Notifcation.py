import time
import pyttsx3
import google.auth
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to retrieve new Gmail messages
def get_new_messages():
    creds = None

    # Check if token.pickle file exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google.auth.default()
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Create Gmail API service
    service = build('gmail', 'v1', credentials=creds)

    # Get the user's Gmail inbox
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No new messages.')
    else:
        print('New messages:')
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            subject = None
            for header in msg['payload']['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
                    break
            if subject:
                print(f'Subject: {subject}')
                engine.say(f'New message with subject: {subject}')
                engine.runAndWait()

# Monitor Gmail notifications
while True:
    get_new_messages()
    time.sleep(60)  # Check for new messages every minute
