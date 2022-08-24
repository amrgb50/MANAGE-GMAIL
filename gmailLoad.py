from gmailAuthentication import authentication
from gmailTransformations import dataTransformation
import pandas as pd

class targetLoad():
    def __init__(self,sqlengine) :
        self.gmailMsgDF = pd.read_csv('data/stageLayer/extract.csv',usecols=['MSG_ID','RECEIVE_DT','FRM_EMAIL'])
        self.sqlconn = sqlengine

    def gmailMsgLoad(self):
        self.gmailMsgDF.to_sql('gmailMsgs',self.sqlconn,if_exists='append', index=False )
        return 1