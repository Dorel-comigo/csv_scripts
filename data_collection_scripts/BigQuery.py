from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= \
    "C:\\Users\dorel.moran\PycharmProjects\csv_scripts\BigQuery\google_key_credentials.json"


client = bigquery.Client()
dataset_id = 'tests'

dataset_ref = client.dataset(dataset_id)
dataset = client.get_dataset(dataset_ref)
print('Dataset ID: {}'.format(dataset_id))
print('Tables:')
tables = list(client.list_tables(dataset_ref))  # API request(s)
if tables:
    for table in tables:
        print('\t{}'.format(table.table_id))
else:
    print('\tThis dataset does not contain any tables.')