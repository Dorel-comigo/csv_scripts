from google.cloud import bigquery
from formatted_string import formatted_name
import os, sys, csv


def table_query(input_A):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
        "C:\\Users\dorel.moran\PycharmProjects\csv_scripts\BigQuery\google_key_credentials.json"
#TODO;: put file in GIT repository

    client = bigquery.Client()
    dataset_id = 'tests'
    dataset_ref = client.dataset(dataset_id)
    table_id = 'test1'
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)
    table_root = dataset_id + '.' + table_id

    query = insert_query(input_A, table_root)
    print(query)

    query_job = client.query(query)
    for row in query_job: print(row)


def insert_query(input_A, table_root):
    with open(input_A + '.csv', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        input_list = []
        '''
        @col_headers --> Change column names here based on input csv file's columns.
        '''
        col_headers = ['item_name', 'item_type', 'item_year', 'fb_annotation']
        for row in reader:
            input_list.append([formatted_name(row(col_headers[0])), row(col_headers[0]),
                              row(col_headers[1]), row(col_headers[2]), row(col_headers[3])])

        '''
    `   @db_col_headers --> Change column names here based on the databse columns to add values for.
        '''
        db_col_headers = ['item_name', 'item_type', 'item_year', 'item_timestamp']
        db_col_headers_sql = '('
        for i in range(len(db_col_headers)):
            db_col_headers_sql += db_col_headers[i] + ','
            if db_col_headers[i] == db_col_headers[-1]:
                db_col_headers_sql = db_col_headers_sql[:-1] + ')'
        return ('INSERT INTO ' + table_root + db_col_headers_sql + ' VALUES ' + y)


def main():
    input_A = sys.argv[1]
    table_query(input_A)

if __name__ == '__main__':
    main()