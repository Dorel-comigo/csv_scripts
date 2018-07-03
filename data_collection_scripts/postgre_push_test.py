import psycopg2, sys, csv
from formatted_string import formatted

def postgre_push(input_file):
    #connection attempt
    conn = ""
    try: conn = psycopg2.connect("dbname='data_collection' user='postgres' host='localhost' password='123'")
    except: print("Uable to connect to the database")
    cur = conn.cursor()

    with open(input_file + '.csv', newline='', encoding='utf-8') as input:
        reader = csv.reader(input)
        csv_list = []
        i = 0
        for row in reader:
            for item in row:
                cur.execute("INSERT INTO data_collection(name, type, year, formatted_name, facebook_id, popularity, test_train) "
                     "VALUES('" + item.split('|')[0] + "','" + item.split('|')[1] + "'," + item.split('|')[2] +
                     ",'" + formatted(item.split('|')[0]) + "','" + item.split('|')[3] + "'," + item.split('|')[4] +
                            ",'train')")



    cur.execute("select * from data_collection")
    rows = cur.fetchall()
    print("\nThe databases:\n")
    for row in rows:
        print("   ", row)

    conn.commit()
def main():
    try:
        if len(sys.argv) >= 2: input_file = sys.argv[1]
        else: input_file = input("Please enter input csv file name:")
        postgre_push(input_file)
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
              ' No files with given input/output name are currently open.')

if __name__ == '__main__':
    main()
