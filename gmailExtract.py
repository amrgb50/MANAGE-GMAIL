from __future__ import print_function
from importlib import import_module
from time import strftime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import dateutil.parser as parser
from gmailAuthentication import  authentication
from datetime import datetime
import json

class gmailExtract() :

    def __init__(self,authcred):
        self.gmailAuthObj = authcred
        self.msgInfoList = []

    def extractUnreadEmails(self):
        try:
            service = build('gmail', 'v1', credentials=self.gmailAuthObj)# Call the Gmail API
            messages = service.users().messages().list(userId ='me', labelIds = ['UNREAD'], maxResults = 500).execute().get('messages',[])
            if len(messages) > 0 :
                for msg in messages :
                    msg_id = msg['id']
                    dt = None
                    frmEmail = None
                    frmName = None
                    #need to improve this part for batch request. 
                    payload = service.users().messages().get(userId = 'me', id = msg_id).execute()
                    #
                    for headers in payload['payload']['headers']:
                        if headers['name'] == 'Date' :
                            parseddatetime = parser.parse(headers['value']) 
                            dt = parseddatetime.date()
                        elif headers['name'] == 'From' :
                            frm = headers['value']
                            __, frmEmail = frm.replace(">",'').split(" <")
                    self.msgInfoList.append([msg_id,dt,frmEmail])  
            else : 
                print("No emails to read!!\nAttention empty msglist is being passed")
            
            rawFileDict = {
                'data' : self.msgInfoList
            }
            with open('data/rawLayer/gmailExtract.txt','w') as f:
                json.dump(rawFileDict, f, default=str)
                return 1
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')
            return 0

    def unreademails(self):
        msg_ids = []
        for msg in self.msgInfoList :
            msg_ids.append(msg[0])
        unreadAction = { 
                "ids" : msg_ids,
                "removeLabelIds" : ["UNREAD"]
            }
        try :
            service = build('gmail', 'v1', credentials=self.gmailAuthObj)
            service.users().messages().batchModify(userId = 'me', body = unreadAction).execute()
        except HttpError as error:
            print(f'An error occurred: {error}')


            