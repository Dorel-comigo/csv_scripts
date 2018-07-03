import csv, sys
from formatted_string import formatted_url
from collections import Counter

'''
@Date: 15.5.18
@Author: Dorel Moran

@Description: .

@Requirements:  

'''

def compress(input_file1, input_file2, output_file):
    with open(input_file1 + '.csv', newline='', encoding='utf-8') as input1:
        with open(input_file2 + '.csv', newline='', encoding='utf-8') as input2:
            reader1 = csv.DictReader(input1)
            reader2 = csv.DictReader(input2)
            with open(output_file + '.csv', 'w' , newline='', encoding='utf-8') as output:
                writer = csv.writer(output)
                dict1 = {}
                for row in reader:  # Way to convert columns to lists
                    for header, value in row.items():
                        try:
                            dict1[header].append(value)
                        except KeyError:
                            dict1[header] = [value]
                tuples1 = [(combine_dups(dict1['Input.VideoID']))]
                tuples1.append(combine_dups(dict1['Input.Name']))
                tuples1.append(combine_dups(dict1['Input.Type']))
                tuples1.append(combine_dups(dict1['Input.Year']))
                tuples1.append(majority(list(zip(dict1[csv_input], dict1[csv_answer]))))
                tuples1 = list(zip(*tuples1))

                writer.writerow(('VideoID', 'Name', 'Type', 'Year', 'Answer.category'))
                writer.writerows(tuples1)


def combine_dups(list):
    result = []
    i = 0
    while i < len(list) :
        try:
            if list[i] == list[i+1] and list[i] == list[i+2]:
                i = i + 2
        except IndexError: pass
        try:
            if list[i] == list[i+1] and list[i] != list[i+2]:
                i = i + 1
        except IndexError: pass
        result.append(list[i])
        i = i + 1
    return result


def majority(tuples):
    i = 0
    result = []
    while i < len(tuples):
        if tuples[i][0] == tuples[i+1][0] == tuples[i+2][0]:
            if formatted_url(tuples[i][1]) != formatted_url(tuples[i + 1][1]) and formatted_url(tuples[i][1]) != formatted_url(tuples[i + 2][1])\
            and formatted_url(tuples[i + 1][1]) != formatted_url(tuples[i + 2][1]):
                result.insert(len(result), ('Inconclusive'))
            else : result.insert(len(result), (Counter(formatted_url(x[1]) for x in tuples[i:i+3]).most_common(1)[0][0]))
            i = i + 3
        elif tuples[i][0] == tuples[i+1][0] != tuples[i+2][0]:
            if formatted_url(tuples[i][1]) != formatted_url(tuples[i + 1][1]):
                result.insert(len(result), ('Inconclusive'))
            else: result.insert(len(result), (formatted_url(tuples[i][1])))
            i = i + 2
        else:
            result.insert(len(result), (formatted_url(tuples[i][1])))
            i = i + 1
    return result


def main():
    try:
        if len(sys.argv) >= 2: input_file1 = sys.argv[1]
        else: input_file1 = input("Please enter first input csv file name:")
        if len(sys.argv) >= 3: input_file2 = sys.argv[2]
        else: input_file2 = input("Please enter second input csv file name:")
        if len(sys.argv) >= 4: output_file = sys.argv[3]
        else: output_file = input("Please enter output csv file name:")

        compress(input_file1, input_file2, output_file)
        print("Successfuly created '" + output_file + "' from '" + input_file1 + "' and '" + input_file2 + "'.", '\n')
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
              ' No files with given input/output name are currently open.')
if __name__ == '__main__':
        main()
