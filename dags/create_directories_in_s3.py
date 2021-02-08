import boto3
import itertools
import datetime


def create_directories_in_s3(**kwargs):
    bucket_name = kwargs['bucket_name']
    s3 = boto3.client('s3')
    date = '{:%B%d%Y}'.format(datetime.now())
    records = [record for record in list(itertools.product(holding_symbols, endpoints))]
    file_pattern_list = []
    for record in records:
        holding_symbol,api_call = record
        directory_string = '{}/{}/{}/'.format(holding_symbol,api_call,date)
        file_pattern_list.append(directory_string)
    for directory in file_pattern_list:
        s3.put_object(Bucket=bucket_name,Key=(directory))
