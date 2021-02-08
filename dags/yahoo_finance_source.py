from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta,datetime
import boto3
import requests
import json
from airflow.models import Variable
from create_directories_in_s3 import create_directories_in_s3
from post_to_s3 import Get_Stocks



'''
Testing setting,getting variables below. If I have time I'll try and externalize all the variables in a much neater way,
not hardcoding things in. 
'''


header_rapidapi_key_key = Variable.set('header_rapidapi_key_key','x-rapidapi-key')
header_rapidapi_key_value = Variable.set('header_rapidapi_key_value','d5e95517a2msh75c98018c625d82p12ab5ejsndd559dc778fd')
header_rapidapi_host_key = Variable.set('header_rapidapi_host_key','x-rapidapi-host')
header_rapidapi_host_value = Variable.set('header_rapidapi_host_value','apidojo-yahoo-finance-v1.p.rapidapi.com')

header_rapidapi_key_key = Variable.get('header_rapidapi_key_key')
header_rapidapi_key_value = Variable.get('header_rapidapi_key_value')
header_rapidapi_host_key = Variable.get('header_rapidapi_host_key')
header_rapidapi_host_value = Variable.get('header_rapidapi_host_value')


holding_symbols = ["AAPL","AMZN","AAL"]
endpoints = ['get_detail','get_history','get_financials']
bucket_name = 'yahoo-finance-data-aef'












default_args = {
    'owner': 'Alexander Fournier',
    'depends_on_past': False,
    'email': ['alexander.fournier@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
}


dag = DAG(
    dag_id='Yahoo_Finance_Pipeline',
    description='Pulling Data from Yahoo Finance API',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
)




with dag:
    t1 = PythonOperator(
        task_id='Create_Directories_in_S3',
        python_callable=create_directories_in_s3,
        op_kwargs={'bucket_name': bucket_name, 'holding_symbols': holding_symbols, 'endpoints': endpoints},
        dag=dag,

    )
    t2 = PythonOperator(
        task_id='Post_to_S3',
        python_callable=Get_Stocks,
        op_kwargs={'bucket':bucket_name,'destination_file':'test1','holding_symbol':'AAPL','country_code':'US'},
        dag=dag,
    )




t1 >> t2
