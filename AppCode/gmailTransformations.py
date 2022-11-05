#this module will do dq and necessary transfromations
import pandas as pd
import json
import configparser
from typing import Any

class dataTransformation :
    def __init__(self, batchdt : str) :
        self.batch_dt : str = batchdt

    def getGmailExtractDF(self):
        config = configparser.ConfigParser()
        config.read('AppCode/config.cfg')
        app_path = config['dev']['APP_PATH']
        ods_path = config['dev']['ODS_PATH']
        stage_path = config['dev']['STAGE_PATH']

        with open(f'{app_path}{ods_path}gmailExtract_{self.batch_dt}.txt','r') as f:
            data = json.load(f)   
        gmExtractList = data['data'] 
        gmailDF = pd.DataFrame(gmExtractList,columns=['MSG_ID','RECEIVE_DT','FRM_EMAIL'])
        gmailDF.to_csv(f'{app_path}{stage_path}gmailStage_{self.batch_dt}.csv')

    