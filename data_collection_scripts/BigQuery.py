from google.cloud import bigquery
import os, sys

def table_query(input_A, input_B):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= \
        "C:\\Users\dorel.moran\PycharmProjects\csv_scripts\BigQuery\google_key_credentials.json"


    client = bigquery.Client()
    dataset_ref = client.dataset('tests')
    table_ref = dataset_ref.table('test1')
    table = client.get_table(table_ref)

    query = (
        'SELECT '
    )


def main():
    if len(sys.argv) >= 2: input_A = sys.argv[1]
    else: input_A = input("Please enter a number for the relevant query to run:"
                          "\n 1 - SELECT"
                          "\n 2 - INSERT"
                          "\n 3 - UPDATE: ")
    if input_A == '1':
        if len(sys.argv) >= 3: input_B = sys.argv[2]
        else: input_B = input("Please enter the names of the requested columns to show: ")
