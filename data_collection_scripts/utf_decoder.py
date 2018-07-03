import sys, csv

'''
@Date: 29.5.18
@Version: 1.0.0
@Author: Dorel Moran

@Description: 

'''

def utf_decoder(input_file, output_file):
    with open(input_file + '.csv', newline='', encoding='utf-8') as input:
        reader = csv.reader(input)
        reader.__next__()
        with open(output_file + '.csv', 'w', newline='', encoding='utf-8') as output:
            writer = csv.writer(output)
            for row in reader:
                print(row[0])
                new_row = row[0].encode('iso-8859-1').decode('utf-8')
                writer.writerow(new_row)





def main():
    try:
        if len(sys.argv) >= 2: input_file = sys.argv[1]
        else: input_file = input("Please enter input csv file name:")
        if len(sys.argv) >= 3: output_file = sys.argv[2]
        else: output_file = input("Please enter output csv file name:")
        utf_decoder(input_file, output_file)
        print("Successfuly created '" + output_file + "-.csv' from '" + input_file + ".csv'.", '\n')
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
                     ' No files with given input/output name are currently open.')

if __name__ == '__main__':
    main()