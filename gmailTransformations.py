#this module will do dq and necessary transfromations
import pandas as pd
from gmailExtract import gmailExtract
from gmailAuthentication import authentication
import json

class dataTransformation :
    def __init__(self) :
        self.gmailDF = None
        self.gmExtractList = []

    def getGmailExtractDF(self):
        with open('data/rawLayer/gmailExtract.txt','r') as f:
            data = json.load(f)   
        self.gmExtractList = data['data'] 
        self.gmailDF = pd.DataFrame(self.gmExtractList,columns=['MSG_ID','RECEIVE_DT','FRM_EMAIL'])
        self.gmailDF.to_csv('data/stageLayer/extract.csv')

    