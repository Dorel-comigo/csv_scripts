from google.cloud import bigquery
from formatted_string import formatted_name
import os, sys, csv


def table_query(input_A, input_B):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
        "C:\\Users\dorel.moran\PycharmProjects\csv_scripts\BigQuery\google_key_credentials.json"

    client = bigquery.Client()
    dataset_id = 'tests'
    dataset_ref = client.dataset(dataset_id)
    table_id = 'test1'
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)
    table_root = dataset_id + '.' + table_id

    query = ''
    if input_A == 'select':
        query = select_query(input_B, input_where, table_root)

    elif input_A == 'insert':
        query = insert_query(input_B, table_root)

    print(query)
    query_job = client.query(query)
    for row in query_job: print(row)

def select_query(input_B, table_root):
    if input_B: pass
    else: input_B = '*'
    #TODO: Add 'WHERE' timestamp column is latest for each item (differentiated by item_id)
    return ('SELECT ' + input_B
             + ' FROM ' + table_root)


def insert_query(input_B, table_root):
    with open(input_B + '.csv', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        input_list = []
        '''
        @col_headers --> Change column names here based on input csv file's columns,
        '''
        col_headers = ['item_name', 'item_type', 'item_year', 'fb_annotation']
        for row in reader: input_list.append([formatted_name(row(col_headers[0])), row(col_headers[0]),
                                              row(col_headers[1]), row(col_headers[2]), row(col_headers[3])])

        return ('INSERT INTO ' + table_root + '(' + ''
                + ' VALUES ' + y)


def update_query():
    pass


def main():
    input_A = sys.argv[1]
    input_B = ''
    #TODO: 'WHERE' input as an additional customization for sql command
    if input_A == 'select':
        if sys.argv[2] != 'where':
            arg_count = len(sys.argv)
            for i in range(arg_count - 2): input_B += sys.argv[i + 2] + ', '
            input_B = input_B[0:-2]  # Remove the last comma and space.
        else: input_B = ''
    elif input_A == 'insert':
        input_B = sys.argv[2]
    else:
        print('Argument ERROR - First argument should only be "select" or "insert"')
        exit(1)
    table_query(input_A, input_B)


if __name__ == '__main__':
    main()