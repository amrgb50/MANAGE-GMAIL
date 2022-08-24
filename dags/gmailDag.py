from email.policy import default
from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import sys
sys.path.insert(1,'/Users/abhaymone/src/dev/sand/MANAGE-GMAIL')
from gmailAuthentication import authentication
from gmailExtract import gmailExtract
from gmailTransformations import dataTransformation
from gmailLoad import targetLoad
"""def pushAuthentication():
    auth = authentication()
    return auth.getgmailAuthentication()

def pushDBConn():
    auth = authentication()
    return  auth.getdbconn()
"""

def pullGmailExtract():
    #pull gmail cred and perfrom api call to extract unread 
    # emails and save file to raw layer
    #gmailauth = ti.xcom_pull(task_ids='pushAuthentication')
    auth = authentication()
    gextract =  gmailExtract(authcred=auth.getgmailAuthentication())
    if gextract.extractUnreadEmails():
        #gextract.unreademails()
        pass

def gmailTransformatn():
    #pickup file from raw layer and do transformation
    #save file to stage layer
    gmailTf = dataTransformation()
    gmailTf.getGmailExtractDF()

def pullGmailLoad():
    #pull dbconn ,pickup file from stage and load to db
    auth = authentication()
    tbLoad = targetLoad(sqlengine=auth.getdbconn())
    tbLoad.gmailMsgLoad()

DAG = DAG(
dag_id='gmailPipelineV1',
start_date=datetime(2022,8,21,16,20,0),
schedule_interval='@daily'
) 
"""
gmailAuthTask = PythonOperator(
        task_id='gmailAuthTask',
        python_callable=pushAuthentication,
        dag = DAG
    )
"""
gmailExtractTask = PythonOperator(
        task_id = 'gmailExtractTask',
        python_callable=pullGmailExtract,
        dag = DAG
    )

gmailTransformationTask = PythonOperator(
        task_id = 'gmailTransformationTask',
        python_callable=gmailTransformatn,
        dag = DAG
    )

gmailTbLoadTask = PythonOperator(
        task_id = 'gmailTbLoadTask',
        python_callable=pullGmailLoad,
        dag = DAG
    )

gmailExtractTask.set_downstream(gmailTransformationTask)
gmailTransformationTask.set_downstream(gmailTbLoadTask)
