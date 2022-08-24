from __future__ import print_function
from email import message
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sqlalchemy import create_engine
import pymysql
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


class authentication :

    def __init__(self) :
        self.gmailcreds = None
        self.sqlengine = None

    def getgmailAuthentication(self):
        gmailcreds = None
        if os.path.exists('token.json'):
            gmailcreds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not gmailcreds or not gmailcreds.valid:
            if gmailcreds and gmailcreds.expired and gmailcreds.refresh_token:
                gmailcreds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'data/credentials.json', SCOPES)
                gmailcreds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(gmailcreds.to_json())    
        self.gmailcreds = gmailcreds
        return self.gmailcreds

    def getdbconn(self):
        self.sqlengine = create_engine("mysql+pymysql://root:passwd@localhost/gmailTables")
        return self.sqlengine

        