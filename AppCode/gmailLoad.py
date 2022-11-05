import pandas as pd
import configparser
from typing import Any


class targetLoad():
    def __init__(self,sqlengine : Any, batchdt : str) :
        self.sqlconn = sqlengine
        self.batch_dt : str = batchdt

    def gmailMsgLoad(self):
        config = configparser.ConfigParser()
        config.read('AppCode/config.cfg')
        app_path = config['dev']['APP_PATH']
        stage_path = config['dev']['STAGE_PATH']
        gmailMsgDF = pd.read_csv(f'{app_path}{stage_path}gmailStage_{self.batch_dt}.csv',usecols=['MSG_ID','RECEIVE_DT','FRM_EMAIL'])
        gmailMsgDF.to_sql('gmailMsgs',self.sqlconn,if_exists='append', index=False )
        return 1