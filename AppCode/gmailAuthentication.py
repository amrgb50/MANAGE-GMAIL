from __future__ import print_function
from email import message
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sqlalchemy import create_engine
import configparser

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class authentication :

    def __init__(self) :
        self.gmailcreds = None
        self.sqlengine = None

    def getgmailAuthentication(self):
        """variable section"""
        configP = configparser.ConfigParser()
        configP.read('AppCode/config.cfg')
        app_path = configP['dev']['APP_PATH']
        api_cred_file = configP['dev']['API_CREDENTIAL_FILE']
        api_token_file = configP['dev']['API_TOKEN_FILE']
        gmailcreds = None
        print(app_path+api_token_file)
        if os.path.exists(app_path+api_token_file):
            gmailcreds = Credentials.from_authorized_user_file(app_path+api_token_file, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not gmailcreds or not gmailcreds.valid:
            if gmailcreds and gmailcreds.expired and gmailcreds.refresh_token:
                gmailcreds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(app_path+api_cred_file, SCOPES)
                gmailcreds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(app_path+api_token_file, 'w') as token:
                token.write(gmailcreds.to_json())    
        self.gmailcreds = gmailcreds
        return self.gmailcreds

    def getdbconn(self):
        configP = configparser.ConfigParser()
        configP.read('AppCode/config.cfg')
        dbusr = configP['dev']['DB_USER']
        dbpass = configP['dev']['DB_PASS']
        dbhost = configP['dev']['DB_HOST']
        dbname = configP['dev']['DB_NAME']
        self.sqlengine = create_engine(f"mysql+pymysql://{dbusr}:{dbpass}@{dbhost}/{dbname}")
        return self.sqlengine

        