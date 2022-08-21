#this module will do dq and necessary transfromations
import pandas as pd
from gmailExtract import gmailExtract
from gmailAuthentication import authentication

class dataTransformation :
    def __init__(self) :
        self.gmailDF = None
        self.gmExtractList = []

    def getGmailExtractDF(self):
        gmExt = gmailExtract()
        self.gmExtractList = gmExt.extractUnreadEmails()
        self.gmailDF = pd.DataFrame(self.gmExtractList,columns=['MSG_ID','RECEIVE_DT','FRM_EMAIL'])
        self.gmailDF.to_csv('data/extract.csv')
        return self.gmailDF

    