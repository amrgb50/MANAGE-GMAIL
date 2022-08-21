from gmailAuthentication import authentication
from gmailTransformations import dataTransformation
import pandas as pd

class targetLoad():
    def __init__(self) :
        dt = dataTransformation()
        self.gmailMsgDF = dt.getGmailExtractDF()

    def gmailMsgLoad(self):
        auth = authentication()
        sqlengine = auth.getdbconn()
        self.gmailMsgDF.to_sql('gmailMsgs',sqlengine,if_exists='append', index=False )
        return 1