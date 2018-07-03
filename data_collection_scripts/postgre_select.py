import psycopg2, sys, csv
from formatted_string import piped_string_to_list

'''
@Date: 3.5.18
@Author: Dorel Moran

@Description: Takes as input a csv file seperated by pipes.
By changing the code- it pushes new row for each item in the input for specified columns to
the SQL table 'data_collection'.

'''

def postgre_select(input_file):
    #connection attempt
    conn = ""
    try: conn = psycopg2.connect("dbname='data_collection' user='postgres' host='localhost' password='123'")
    except: print("Uable to connect to the database")
    cur = conn.cursor()

    with open(input_file + '.csv', newline='', encoding='utf-8') as input:
        reader = csv.reader(input)
        csv_list = []
        for [row] in reader:
            csv_list.append(piped_string_to_list(row))

        '''
        Specify what SQL columns and what info to show here in the code after 
            'SELECT....
        '''
        cur.execute("SELECT "
                    # Modify column names. * for every column.
                    "*"
                    #
        
                    ### 
                    " FROM data_collection "
                    ###
        
                    # Optiona; specific cell search. (i.e: WHERE @column_name = '@cell_name')
                    "WHERE name = 'The Big Bang Theory'")
                    #

        rows = cur.fetchall()
        print("\nThe database:\n")
        for row in rows:
            print("   ", row)

def main():
    try:
        if len(sys.argv) >= 2: input_file = sys.argv[1]
        else: input_file = input("Please enter input csv file name:")
        postgre_select(input_file)
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
              ' No files with given input/output name are currently open.')

if __name__ == '__main__':
    main()
