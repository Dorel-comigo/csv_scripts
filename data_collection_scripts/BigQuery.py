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
        '''
        - In case the headers are in the .csv file- use following code and comment out the later @csv_col_header code.
        - Get csv column header if the first row is indeed the headers.
        - Added inclusions in case the header name is not formatted correctly.
        '''
        csv_col_headers = reader.__next__()
        for n, header in enumerate(csv_col_headers):
            '''
            Add inclusions here if needed:
            '''
            if header == 'name' or header == 'Name':
                csv_col_headers[n] = 'item_name'
            elif header == 'type' or header == 'Type':
                csv_col_headers[n] = 'item_type'
            elif header == 'year' or header == 'Year':
                csv_col_headers[n] = 'item_year'
            if '-' in header:
                csv_col_headers[n] = csv_col_headers[n].replace('-', '_')
            if ' ' in header:
                csv_col_headers[n] = csv_col_headers[n].replace(' ', '_')
        '''
        - In case no headers are in the csv file- use following code and comment out the former @csv_col_headers code.
        - Manualy pick the csv header names:
        '''
        # csv_col_headers = ['item_name', 'item_type', 'item_year', 'fb_annotation']

        '''
        @original_db_col_headers = database column names before any columns have been added from the script.
        '''
        original_db_col_headers = []
        for i in range(len(table.schema)):
            original_db_col_headers.append(table.schema[i].name)

        '''
        Adds a new column in case the .csv file gives a header the database doesn't currently have.
        '''
        for i in range(len(csv_col_headers)):
            if csv_col_headers[i] not in original_db_col_headers:
                original_schema = table.schema
                new_schema = original_schema[:]
                new_schema.append(bigquery.SchemaField(csv_col_headers[i], 'STRING'))
                table.schema = new_schema
                table = bigquery.Client().update_table(table, ['schema'])
                print('Added new column:', csv_col_headers[i])

        '''
        @current_db_col_headers = database column names after the new headers have been added.
        - The @current_db_col_headers is being modified so its values will be in a specific order to correlate with the
        values that are being added to the database.
        - Order of values: 'item_id', 'item_timestamp', evety other column from the .csv file ordered by the .csv order.
        '''
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

        '''
        Turns the @current_db_col_headers to one string formatted for SQL query.
        '''
        current_db_col_headers_sql = '('
        for i in range(len(current_db_col_headers)):
            current_db_col_headers_sql += current_db_col_headers[i] + ','
            if current_db_col_headers[i] == current_db_col_headers[-1]:
                current_db_col_headers_sql = current_db_col_headers_sql[:-1] + ')'


        select_latest_query = "SELECT " + current_db_col_headers_sql + " FROM " + table.dataset_id + '.' + table.table_id + \
                              " s1 WHERE item_timestamp = (SELECT max(item_timestamp) " \
                              "FROM " + table.dataset_id + '.' + table.table_id + " s2 WHERE s1.item_id = s2.item_id)"
        select_job = client.query(select_latest_query)
        select_job.result()
        latest_db_items = []
        for latest_item in select_job:
            item_to_add = []
            for i in range(len(latest_item[0])):
                item_to_add.append(latest_item[0]['_field_' + str(i + 1)])
            latest_db_items.append(item_to_add)
        db_items_id = [item[0] for item in latest_db_items]

        csv_items = []
        csv_items_id = []
        #reader.__next__()
        item_to_add = []
        for row in reader:
            for j in range(len(row)):
                if "''" in row[j]:
                    row[j] = row[j].replace("''", "'")
                row[j] = row[j].replace("'", r"\'")
                row[j] = row[j].replace('film', 'movie')
                row[j] = row[j].replace('series', 'show')
            csv_items_id.append(formatted_name(row[0]) + row[2])
            if csv_items_id[-1] in db_items_id:   # check if the inserted item's id is already in the db.
                for db_item in latest_db_items:
                    if db_item[0] == csv_items_id[-1]:  # check if the db item is the inserted item.
                        item_to_add = ["'" + db_item[0] + "'"]
                        item_to_add.append('CURRENT_TIMESTAMP')
                        i = 2
                        for header in current_db_col_headers[2:]:
                            if db_item[i] != '' and db_item[i] != None:
                                db_item[i] = db_item[i].replace("'", r"\'")
                                item_to_add.append("'" + db_item[i] + "'")
                            else:
                                if header in csv_col_headers:
                                    item_to_add.append("'" + row[i - 2] + "'")
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