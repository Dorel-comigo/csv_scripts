import csv, sys
from formatted_string import formatted_url
from collections import Counter

'''
@Date: 22.5.18
@Version: 1.3.3
@Author: Dorel Moran

@Description: Takes as input: A. a .csv file.  B. an input column name.  C. an answer column name. 
Outputs a .csv file with 2 columns only, Input column and an answer column, that follows the next ruling:
Removes duplicated inputs. 
The answers for the same input are getting chosen by a majority method, where if most (>50%) answers are identical- 
then that is the answer to that input.
If no answer to that input is in a majority (<=50%) then the answer to the input is written as 'inconclusive'.

@Requirements:  
-If there isn't a answer to be found- the url should include 'none' in its name.
-The duplicated inputs shouldn't exceed 3.
'''

def compress(file, csv_input, csv_answer):
    with open(file + '.csv', newline='', encoding='utf-8') as input:
        reader = csv.DictReader(input)
        with open(file + '_Compressed.csv', 'w' , newline='', encoding='utf-8') as output:
            writer = csv.writer(output)
            dict1 = {}
            for row in reader:  # Way to convert columns to lists
                for header, value in row.items():
                    try:
                        dict1[header].append(value)
                    except KeyError:
                        dict1[header] = [value]
            tuples1 = []

            '''
            Here are the wanted columns by input column name. 
            When wanting different columns- change the string name. 
            To change number of columns- delete line or copy/paste another line.
            '''
            tuples1.append(combine_dups(dict1['HITId']))
            tuples1.append(combine_dups(dict1['Input.file_name']))
            tuples1.append(combine_dups(dict1['Input.line_number']))
            tuples1.append(combine_dups(dict1['Input.mention']))

            '''
            Here's the answer column. Based on user's input of column names.
            '''

            tuples1.append(majority(list(zip(dict1[csv_input], dict1['Answer.match']))))
            tuples1.append(majority(list(zip(dict1[csv_input], dict1[csv_answer]))))
            tuples1.append(combine_dups(dict1['Input.machine_tag']))
            tuples1 = list(zip(*tuples1))

            ''' 
            Output's column names. 
            '''
            writer.writerow(('HITId', 'file_name', 'line_number', 'mention', 'answer_match', 'answer_tag', 'machine_tag'))
            writer.writerows(tuples1)
            print("\nSuccessfuly created '" + file + "_Compressed.csv' from '" + file + ".csv'.", '\n')



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
        if len(sys.argv) >= 2: file = sys.argv[1]
        else: file = input("Please enter input csv file name:")
        if len(sys.argv) >= 3: csv_input = sys.argv[2]
        else: csv_input = input("Please enter header name of tested column from: " + file)
        if len(sys.argv) >= 4: csv_answer = sys.argv[3]
        else: csv_answer = input("Please enter header name of answer column from: " + file)

        compress(file, csv_input, csv_answer)
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
              ' No files with given input/output name are currently open.')
if __name__ == '__main__':
        main()
else:
    print('Using \'compressed_results.py\' method:', '\n')
    main()
