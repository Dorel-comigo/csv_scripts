import sys, csv

'''
@Date: 3.5.18
@Author: Dorel Moran

@Description: Formats strings for SQL usage, mturk usage, etc.

'''

def cellc_dump_fix(input_file, output_file):
    with open(input_file + '.csv', newline='', encoding='ISO-8859-1') as input:
        reader = csv.reader(input)
        header = reader.__next__()
        row_list = [('name', 'type', 'year', 'twitter_annotation_Revital',
                     'popularity', 'vote_count')]
        for row in reader:
            fb_anno = ''
            tw_anno = ''
            fb_manual = 'FALSE'
            tw_manual = 'FALSE'
            i = 0
            try:

                if (row[i].split('|')[11]) == 'TRUE': fb_manual = 'TRUE'
                if (row[i].split('|')[17]) == 'TRUE': tw_manual = 'TRUE'
                if (row[i].split('|')[14]) == 'FP' or (row[i].split('|')[14]) == 'FN':
                    if row[i].split('|')[15] == '': tw_anno = 'x'
                    else: tw_anno = row[i].split('|')[15]
                elif (row[i].split('|')[14]) == 'TP': tw_anno = row[i].split('|')[12]
                elif (row[i].split('|')[14]) == 'TN': tw_anno = 'x'
                else: pass
                if fb_manual == 'TRUE' and tw_manual == 'TRUE': pass
                else: row_list.append(((row[i].split('|')[5]), (row[i].split('|')[2]), (row[i].split('|')[1]),
                                       tw_anno, (row[i].split('|')[19]), (row[i].split('|')[20])))
                print('row_list latest: ', row_list[-1])
                i = i + 1
            except IndexError : pass

        piped_list = []
        temp = ''
        for row in row_list:
            for x in row:
                temp = temp + x + '|'
            piped_list.append((temp[:-1]))
            temp = ''
            print('piped_list latest:, ', piped_list[-1])

        with open(output_file + '.csv', 'w', newline='', encoding='utf-8') as output:
            writer = csv.writer(output)
            for item in piped_list:
                writer.writerow([item])



def main():
    try:
        if len(sys.argv) >= 2: input_file = sys.argv[1]
        else: input_file = input("Please enter input csv file name:")
        if len(sys.argv) >= 3: output_file = sys.argv[2]
        else: output_file = input("Please enter output csv file name:")
        cellc_dump_fix(input_file, output_file)
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
        ' No files with given input/output name are currently open.')

if __name__ == '__main__':
    main()
