from google.cloud import bigquery
from formatted_string import formatted_name
import os, sys, csv, inspect, re

'''
@Date: 17.7.18
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
    dataset_id = 'tests'
    dataset_ref = client.dataset(dataset_id)
    table_id = 'test1'
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)   #API call


    query = insert_query(input_A, table, client)
    print('\n' + query + '\n')

    query_job = client.query(query)
    query_job.result()   # wait for job to finish
    if query_job.state == 'DONE' : print('Insert query finished successfuly.')
    else: print(query_job.state)

def insert_query(input_A, table, client):
    with open(input_A, newline='', encoding='utf-8-sig') as csv_file:
        reader = csv.reader(csv_file)

        csv_col_headers = reader.__next__()
        for n, header in enumerate(csv_col_headers):
            if header == 'name':
                csv_col_headers[n] = 'item_name'
            elif header == 'type':
                csv_col_headers[n] = 'item_type'
            elif header == 'year':
                csv_col_headers[n] = 'item_year'
        #csv_col_headers = ['item_name', 'item_type', 'item_year', 'tw_annotation']

        original_db_col_headers = []
        for i in range(len(table.schema)):
            original_db_col_headers.append(table.schema[i].name)

        for i in range(len(csv_col_headers)):
            if csv_col_headers[i] not in original_db_col_headers:
                original_schema = table.schema
                new_schema = original_schema[:]
                new_schema.append(bigquery.SchemaField(csv_col_headers[i], 'STRING'))
                table.schema = new_schema
                table = bigquery.Client().update_table(table, ['schema'])
                print('Added new column:', csv_col_headers[i])

        current_db_col_headers = []
        for i in range(len(table.schema)):
            current_db_col_headers.append(table.schema[i].name)
        current_db_col_headers.remove('item_id')
        current_db_col_headers.insert(0, 'item_id')
        current_db_col_headers.remove('item_timestamp')
        current_db_col_headers.insert(1, 'item_timestamp')
        new_index = 2
        for header in csv_col_headers:
            if (header != 'item_id') and (header != 'item_timestamp'):
                current_db_col_headers.remove(header)
                current_db_col_headers.insert(new_index, header)
                new_index += 1

        current_db_col_headers_sql = '('
        for i in range(len(current_db_col_headers)):
            current_db_col_headers_sql += current_db_col_headers[i] + ','
            if current_db_col_headers[i] == current_db_col_headers[-1]:
                current_db_col_headers_sql = current_db_col_headers_sql[:-1] + ')'

        db_row_id = client.list_rows(table, selected_fields=table.schema[:1])
        db_items_id = []
        for row in db_row_id:
            db_items_id.append(row[0])

        csv_items = []
        csv_items_id = []
        #reader.__next__()
        item_to_add = []
        for row in reader:
            csv_items_id.append(formatted_name(row[0]))
            if csv_items_id[-1] in db_items_id:
                for db_row in client.list_rows(table):
                    if db_row['item_id'] == csv_items_id[-1]:
                        item_to_add = ["'" + db_row['item_id'] + "'"]
                        item_to_add.append('CURRENT_TIMESTAMP')
                        i = 0
                        for header in current_db_col_headers[2:]:
                            if db_row[header] != '':
                                try:
                                    item_to_add.append("'" + db_row[header] + "'")
                                except TypeError:
                                    item_to_add.append("''")
                            else:
                                if header in csv_col_headers:
                                    item_to_add.append("'" + row[i] + "'")
                                else:
                                    item_to_add.append("''")
                            i += 1
            else:
                item_to_add = ["'" + csv_items_id[-1] + "'"]
                item_to_add.append('CURRENT_TIMESTAMP')
                for i in range(len(current_db_col_headers) - 2):
                    try:
                        item_to_add.append("'" + row[i] + "'")
                    except IndexError:
                        item_to_add.append("''")
            csv_items.append(item_to_add)

        csv_items_sql = ''
        for i in range(len(csv_items)):
            for j in range(len(csv_items[i])):
                if "''" in csv_items[i][j]:
                    csv_items[i][j] = re.sub(r"\'(\'[a-zA-Z])",r"\\\1", csv_items[i][j])
            csv_items_sql += '(' + ','.join(csv_items[i]) + '),'
            if csv_items[i] == csv_items[-1]:
                csv_items_sql = csv_items_sql[:-1]

        return ('INSERT INTO ' + table.dataset_id + '.' + table.table_id + current_db_col_headers_sql +
                ' VALUES ' + csv_items_sql)


def main():
    input_A = sys.argv[1]
    table_query(input_A)

if __name__ == '__main__':
    main()