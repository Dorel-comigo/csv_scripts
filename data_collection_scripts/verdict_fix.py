import csv, sys

'''
@Date: 2.5.18
@Author: Dorel Moran

@Description: Takes a verdict result csv file with correct answers and outputs a csv with a corrected answer column.

Input: a csv which have 4 columns (precise columns name unimportant): Name, Answer, Verdict, Correct answer.
Verdict column should only have 'Correct' or 'Wrong' in it.
Correct answer should only have corrected answer if it was next to 'Wrong' in the verdict column, and empty if it was 
next to 'Correct'.

Output: a csv which have only 2 columns: Name and Answer, where answer column are the fixed answers.
'''

def verdict_fix(input_file, output_file):
    with open(input_file + '.csv', newline='', encoding='utf-8') as input:
        reader = csv.reader(input)
        result = [('Name', 'Result')]
        for row in reader:
            if row[2] == 'Correct':
                result.append((row[0], row[1]))
            elif row[2] == 'Wrong':
                result.append((row[0], row[3]))
        with open(output_file, "w", newline='', encoding="utf-8") as output:
            writer = csv.writer(output)
            writer.writerows(result)


def main():
    try:
        if len(sys.argv) >= 2: input_file = sys.argv[1]
        else: input_file = input("Please enter input csv file name:")
        output_file = input_file.replace('Compressed_verdict', 'Compressed_fixed.csv')

        verdict_fix(input_file, output_file)
        print("Successfuly created '" + output_file + "' from '" + input_file + "'.", '\n')
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
              ' No files with given input/output name are currently open.')


if __name__ == '__main__':
    main()