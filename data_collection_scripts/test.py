from google.cloud import bigquery
from formatted_string import formatted_name
import os, sys, csv, inspect, re

'''
@Date: 24.7.18
@Version: 1.0.0
@Author: Dorel Moran

@Description: Insert csv files into bigquery database.

'''

def table_query(input_A):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
        "C:\\Users\dorel.moran\PycharmProjects\csv_scripts\BigQuery\google_key_credentials.json"
    #TODO;: put file in GIT repository

    '''   
    @dataset_id , @table_id = names of the BigQuery dataset,table that will be used in the code.
    @dataset_ref, table_ref = references to dataset,table classes.
    @table = Class for given table.
    '''
    client = bigquery.Client()
    dataset_id = 'Database'
    dataset_ref = client.dataset(dataset_id)
    table_id = 'twitter_accounts'
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)   #API call

    '''
    'insert_query' method : returns a string which is an SQL insert query based on the given .csv file,
    table class and client.
    '''
    query = insert_query(input_A, table, client)
    print('\n' + query + '\n')

    '''
    Uses the 'query' string as an SQL query for the current table. Prints out the results of the query
    '''
    query_job = client.query(query)
    query_job.result()   # wait for job to finish.
    if query_job.state == 'DONE' : print('Insert query finished successfuly.')
    else: print(query_job.state)
    # prints state of query if error occured. If omitted- no errors will be shown even if there are.


def insert_query(input_A, table, client):
    with open(input_A, newline='', encoding='utf-8-sig') as csv_file:
        reader = csv.reader(csv_file)
        reader.__next__()

        row_sql = ''
        for row in reader:
            row_sql += "('" + row[0] + "','" + row[1] + "',CURRENT_TIMESTAMP),"
        row_sql = row_sql[:-1]

        return ('INSERT INTO ' + table.dataset_id + '.' + table.table_id + '(tw_name,item_type,item_timestamp)' +
                ' VALUES ' + row_sql)


def main():
    input_A = sys.argv[1]
    table_query(input_A)

if __name__ == '__main__':
    main()