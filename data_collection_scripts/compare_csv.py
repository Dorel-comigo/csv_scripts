import csv, sys
from formatted_string import piped_to_list
from formatted_string import list_to_piped


def compare(input1, input2):
    with open(input1 + '.csv', newline='', encoding='utf-8') as in1:
        with open(input2 + '.csv', newline='', encoding='utf-8') as in2:
            reader1 = csv.reader(in1)
            reader2 = csv.reader(in2)



def main():
    try:
        if len(sys.argv) >= 2: input1 = sys.argv[1]
        else: input1 = input("Please enter first csv file name:")
        if len(sys.argv) >= 3: input2 = sys.argv[2]
        else: input2 = input("Please enter second csv file name:")
        compare(input1, input2)
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B. No files with given input/output name are currently open.')
        exit(1)
if __name__ == '__main__':
        main()

