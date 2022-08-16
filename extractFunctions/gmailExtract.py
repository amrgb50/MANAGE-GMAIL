from __future__ import print_function
from email import message
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

def extractUnreadEmails(creds):
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        message_ids = service.users().messages().list(userId ='me', labelIds = ['UNREAD'], maxResults = 500).execute().get('messages',[])
        if len(message_ids) > 0 :
            msg_ids = []
            msglist = []
            for msg in message_ids :
                msg_id = msg['id']
                msg_ids.append(msg_id)
                payload = service.users().messages().get(userId = 'me', id = msg_id).execute()
                id = payload['id']
                labelIds = payload['labelIds']
                for headers in payload['payload']['headers']:
                    if headers['name'] == 'Date' :
                        dt = headers['value']
                    elif headers['name'] == 'From' :
                        frm = headers['value']
                msglist.append([msg_id,id,labelIds,dt,frm])
            df = pd.DataFrame(msglist,columns=['msg_id','payloadid','labels','receivedDt','from'])
            df.to_csv('data/extract.csv', encoding='utf-8')
        else : 
            print("No emails to read")
            return
        """ unreadAction = { 
            "ids" : msg_ids,
            "removeLabelIds" : ["UNREAD"]
        }
        response =  service.users().messages().batchModify(userId = 'me', body = unreadAction).execute()
        print(response)
        """

    
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')