import csv, sys, re

'''
@Date: 21.6.18
@Version: 1.3.5
@Author: Dorel Moran

@Description: Given a sub file annotated my the machine as input- the script outputs a .csv file ready for mturk testing.
Output .csv includes the following columns: file name, line number of the tag, mention (words) of the tag, 
5 'rows' columns of the sub file that in one of them- the tagged words are in. 
(These rows are in HTML format to grey out rows that DON'T have the tag and in bold when there IS a tag in them. The tag
will be colored red.) and finally a column for which tag the machine gave.
'''

def sub_annotation(input_file, output_file):
    with open(input_file + '.name', encoding='utf-8') as input:
        raw_text = input.readlines()
        raw_text_fixed = []
        # @raw_text_fixed is raw_text without any '__O' (symbol for no tag) and '\n' in it.
        '''
        The difference between the 3 re.sub methods used to remove '__O's exists since there are several instances 
        of this occurance in the sub file. 1. For "The__O man..." should delete and leave space in.
        2. For "Hi__O , guy..." The space should be removed. 3. For "...bye__O " the space should be removed.
        '''
        for line in raw_text:
            line = line.replace('\n', '')
            line = re.sub(r'__O(\s[a-zA-Z])', r'\1', line)
            line = re.sub(r'__O\s([^a-zA-Z])', r'\1', line)
            line = re.sub(r'__O$', r'', line)
            raw_text_fixed.append(line)

        '''
        @tagged_list is the list containing all of the other lists, from which the output is writing.
        @tagged_line_num is the list of the number of lines that are tagged.
        @tags is the list of of all the tags the machine gave (PER, LOC or ORG).
        @tagged_word is the list of the mentions of tagged words.
        @i used to track line number. (When tagged line is the first, second, last or before-last- the tagged_list would 
        be handed differently- the order of the 5 lines would change.)
        '''
        tagged_list = []
        tagged_line_num = []
        tags = []
        tagged_word = []
        i = 0
        for line in raw_text_fixed:
            if '__' in line:
                tag_counter = line.count('__B-')
                tagged_line = line
                for j in range(tag_counter):
                    tags.append(line.split('__B-')[1].split(' ')[0])
                    tagged_word.append(tag_color(line)[1])
                    tagged_line_num.append(i + 1)
                    tagged_line = '<b>' + tag_color(line)[0] + '</b><br>'
                    tagged_line = re.sub(r'__[BI]-...', '', tagged_line)
                    if i == 0:
                        tagged_list.append([tagged_line_num[-1], tags[-1], tagged_word[-1],
                                            [tagged_line, no_tag_color(raw_text_fixed[i + 1]),
                                             no_tag_color(raw_text_fixed[i + 2]), no_tag_color(raw_text_fixed[i + 3]),
                                             no_tag_color(raw_text_fixed[i + 4])]])
                    elif i == 1:
                        tagged_list.append([tagged_line_num[-1], tags[-1], tagged_word[-1],
                                            [no_tag_color(raw_text_fixed[i - 1]), tagged_line,
                                             no_tag_color(raw_text_fixed[i + 1]), no_tag_color(raw_text_fixed[i + 2]),
                                             no_tag_color(raw_text_fixed[i + 3])]])
                    elif i == len(raw_text_fixed) - 2:
                        tagged_list.append([tagged_line_num[-1], tags[-1], tagged_word[-1],
                                            [no_tag_color(raw_text_fixed[i - 3]), no_tag_color(raw_text_fixed[i - 2]),
                                             no_tag_color(raw_text_fixed[i - 1]), tagged_line,
                                             no_tag_color(raw_text_fixed[i + 1])]])
                    elif i == len(raw_text_fixed) - 1:
                        tagged_list.append([tagged_line_num[-1], tags[-1], tagged_word[-1],
                                            [no_tag_color(raw_text_fixed[i - 4]), no_tag_color(raw_text_fixed[i - 3]),
                                             no_tag_color(raw_text_fixed[i - 2]), no_tag_color(raw_text_fixed[i - 1]),
                                             tagged_line]])
                    else:
                        tagged_list.append([tagged_line_num[-1], tags[-1], tagged_word[-1],
                                            [no_tag_color(raw_text_fixed[i - 2]), no_tag_color(raw_text_fixed[i - 1]),
                                             tagged_line, no_tag_color(raw_text_fixed[i + 1]),
                                             no_tag_color(raw_text_fixed[i + 2])]])
                    line = re.sub(r'__B-...', '', line, count=1)
                    if '__I' in line.split('__B')[0]:
                        word_counter = line.split('__B')[0].count('__I')
                        line = re.sub(r'__I-...', '', line, count = word_counter)
            i += 1

        with open(output_file + '.csv', 'w', newline='', encoding='utf-8') as output:
            writer = csv.writer(output)
            '''
            Update here the column headers.
            '''
            writer.writerow(['file_name', 'line_number', 'mention', 'line1', 'line2', 'line3', 'line4', 'line5', 'machine_tag'])
            for item in tagged_list:
                '''
                Update here the column values
                '''
                writer.writerow(['true_detective/' + input.name, item[0], item[2], item[3][0], item[3][1], item[3][2], item[3][3], item[3][4], item[1]])
            print("\nSuccessfuly created '" + output_file + ".csv' from '" + input_file + ".csv'.")


def no_tag_color(str):
    result = '<font color ="gray">' + str + '</font><br>'
    result = re.sub(r'__[BI]-...', '', result)
    return result


def tag_color(string):
    substring = ''
    text = ''
    if '__I' in string.split('__B')[1]:  # If the tag is several words.
        word_counter = string.split('__B')[1].count('__I-')
        if word_counter == 1: modified_string = string
        else: modified_string = re.sub(r'__I-...', '', string, count = (word_counter - 1))
        # @modified_string is the string without '__I-...' except for the last occurange for that tag.
        substring = modified_string.split('__I', 1)[0]
        substring = substring.split('__B', 1)[0].split(' ')[-1] + '__B' + substring.split('__B', 1)[1]
        substring = re.sub(r'__B-...', '', substring)
        if string.split('__B', 1)[0].rsplit(' ', 1)[0] == string.split('__B', 1)[0].rsplit(' ')[-1]:  # If the tagged word is the first.
            text = '<font color="red">' + substring + '</font> ' + modified_string.split('__I', 1)[1].split(' ', 1)[1]
        else:  # If tagged word isn't the first
            text = modified_string.split('__B', 1)[0].rsplit(' ', 1)[0] + ' <font color="red">' + substring + '</font> ' + \
                   modified_string.split('__I', 1)[1].split(' ', 1)[1]
    else:  # If the tag is only one word.
        if string.split('__B', 1)[0].rsplit(' ', 1)[0] == string.split('__B', 1)[0].rsplit(' ')[-1]:  # If the tagged word is the first.
            substring = string.split('__B', 1)[0].split(' ')[-1]
            text = '<font color="red">' + substring + '</font> ' + \
                   string.split('__B', 1)[1].split(' ', 1)[1]
        else:  # If tagged word isn't the first
            substring = string.split('__B', 1)[0].split(' ')[-1]
            text = string.split('__B', 1)[0].rsplit(' ', 1)[0] + ' <font color="red">' + substring \
                    + '</font> ' + string.split('__B', 1)[1].split(' ', 1)[1]
    return [text, substring]




def main():
    try:
        if len(sys.argv) >= 2: input_file = sys.argv[1]
        else: input_file = input("Please enter input file name:")
        if len(sys.argv) >= 3: output_file = sys.argv[2]
        else: output_file = input("Please enter output csv file name:")
        sub_annotation(input_file, output_file)
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
              ' No files with given input/output name are currently open.')
        exit(1)
if __name__ == '__main__':
        main()