import csv, sys

'''
@Date: 21.6.18
@Version: 1.0.0
@Author: Dorel Moran

@Description: 
'''

def annotation_to_pipe_delimited(input_file, output_file):
    with open(input_file + '.csv', newline='', encoding='utf-8') as input:
        reader = csv.DictReader(input)
        output_dict = {}
        for row in reader:
            for header, value in row.items():
                try:
                    output_dict[header].append(value)
                except KeyError:
                    output_dict[header] = [value]
        print(output_dict)








def main():
    try:
        if len(sys.argv) >= 2: input_file = sys.argv[1]
        else: input_file = input("Please enter input csv file name:")
        if len(sys.argv) >= 3: output_file = sys.argv[2]
        else: output_file = input("Please enter output csv file name:")
        annotation_to_pipe_delimited(input_file, output_file)
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
              ' No files with given input/output name are currently open.')

if __name__ == '__main__':
    main()
