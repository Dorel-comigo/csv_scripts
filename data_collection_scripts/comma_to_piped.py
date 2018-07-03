import csv, sys
from formatted_string import list_to_piped_string

'''
@Date: 13.5.18
@Version: 1.0.2
@Author: Dorel Moran

@Description: Takes a comma-delimeted csv file. Outputs a pipe-delimited csv file.

'''

def comma_to_piped(input_file, output_file):
    with open(input_file + '.csv', newline='', encoding='utf-8') as input:
        reader = csv.reader(input)
        out = []
        for row in reader: out.append(list_to_piped_string(row))
        with open(output_file + '.csv', 'w', newline='', encoding='utf-8') as output:
            writer = csv.writer(output)
            for row in out: writer.writerow([row])



def main():
    try:
        if len(sys.argv) >= 2: input_file = sys.argv[1]
        else: input_file = input("Please enter input csv file name:")
        if len(sys.argv) >= 3: output_file = sys.argv[2]
        else: output_file = input("Please enter output csv file name:")
        comma_to_piped(input_file, output_file)
        print("\nSuccessfuly created '" + output_file + "'.csv from '" + input_file + ".csv'.", '\n')
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
              ' No files with given input/output name are currently open.')
if __name__ == '__main__':
        main()