from __future__ import print_function
from email import message
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import dateutil.parser as parser
import datetime

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
                dt = None
                frm = None
                #need to improve this part for batch request. 
                payload = service.users().messages().get(userId = 'me', id = msg_id).execute()
                #
                #to check  : epoch to datetime
                #print(int(payload["internalDate"]))
                #my_time = datetime.datetime.fromtimestamp(int(payload["internalDate"]))
                #labelIds = payload['labelIds']
                for headers in payload['payload']['headers']:
                    if headers['name'] == 'Date' :
                        dt = parser.parse(headers['value']) 
                    elif headers['name'] == 'From' :
                        frm = headers['value']           
                msglist.append([msg_id,dt.date(),frm])
            df = pd.DataFrame(msglist,columns=['msg_id','receivedDt','from'])
            df.set_index('msg_id')
            df['receivedDt']= df['receivedDt'].astype('datetime64[ns]')
            print(df.info())
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