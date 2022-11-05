from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import dateutil.parser as parser
import json
import configparser
from typing import Any

class gmailExtract() :

    def __init__(self,authcred , batchdt : str):
        self.gmailAuthObj = authcred
        self.batch_dt : str = batchdt
        self.msgInfoList : list[Any] = []

    def extractUnreadEmails(self):
        """variable section"""
        config = configparser.ConfigParser()
        config.read('AppCode/config.cfg')
        app_path = config['dev']['APP_PATH']
        ods_path = config['dev']['ODS_PATH']


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
                            print(dt)
                        elif headers['name'] == 'From' :
                            frm = headers['value']
                            if "<" in frm and " " in frm :
                                __, frmEmail = frm.replace(">",'').split("<")                      
                            else:
                                frmEmail = frm
                    self.msgInfoList.append([msg_id,dt,frmEmail])  
                rawFileDict = {
                'data' : self.msgInfoList
                }

                with open(f'{app_path}{ods_path}gmailExtract_{self.batch_dt}.txt','w') as f:
                    json.dump(rawFileDict, f, default=str)
                return 1
            else : 
                print("No emails to read!!\nAttention empty msglist is being passed")
                return 0
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


            