import psycopg2
from formatted_string import formatted_name

'''
@Date: 3.5.18
@Author: Dorel Moran

@Description: Fixes the formatted_name column in saved SQL for a list of rows in the SQL table 'data_collection'.

'''

def sql_formatted_name_fix():
    conn = ""
    try: conn = psycopg2.connect("dbname='data_collection' user='postgres' host='localhost' password='123'")
    except: print("Uable to connect to the database")
    cur = conn.cursor()

    name_list = []
    cur.execute('SELECT formatted_name from data_collection')
    rows = cur.fetchall()
    for row in rows: name_list.append(row)
    print(name_list)
    for name in name_list:
        for x in name:
            print(x)
            x = x.replace("'", "''")
            cur.execute("UPDATE data_collection SET formatted_name = '" + formatted_name(x) + "' WHERE formatted_name = '" + x + "'")

    cur.execute("select * from data_collection")
    rows = cur.fetchall()
    print("\nThe databases:\n")
    for row in rows:
        print("   ", row)
    conn.commit()