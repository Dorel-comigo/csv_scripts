from lxml import html
import requests, sys, csv

'''
@Date: 7.6.18
@Version: 1.1.0
@Author: Dorel Moran

@Description: Takes a .csv file with columns 'title'/'type'/'wiki-en'(wiki page ID) for persons.
Outputs a similiar csv list with another column- 'year', taken by scraping the given wiki page.

NOTICE- Does not give year 100% of the time, in cases the HTML is different in that wiki page. 
Also, if wiki page leads to different page than the person's page- gives false results.
Also, some persons doesn't have birthday in their wiki page, giving false results.

In short- fixing the output csv after execution is mandatory.

'''

def person_birthday_from_wiki(input_file, output_file):
    with open(input_file + '.csv', newline='', encoding='utf-8') as input:
        reader = csv.DictReader(input)
        with_year_list = [['title', 'type', 'year', 'wiki-en']]
        URL = 'https://en.wikipedia.org/wiki/'
        count = 1

        for row in reader:
            print('count:', count)
            request = requests.get(URL + row['wiki-en'])
            html_ele = html.fromstring(request.content)
            raw_html = html_ele.xpath('//text()')
            html_list = []
            for raw_item in raw_html:  # Remove items that contain only spaces/tabs/new_lines or that are empty.
                item = raw_item.replace(' ', '')
                item = item.replace('\n', '')
                item = item.replace('\t', '')
                if not item:
                    pass
                else:
                    html_list.append(item)

            i = 0
            for item in html_list:
                if item == 'Born':
                    try:
                        with_year_list.append([row['\ufefftitle'], row['type'], int(html_list[i + 2][:4]), row['wiki-en']])
                    except ValueError:
                        with_year_list.append([row['\ufefftitle'], row['type'], html_list[i + 3][:4], row['wiki-en']])
                    break
                i = i + 1
            print('latest year list:', with_year_list[-1])
            count = count + 1


        with open(output_file + '.csv', 'w', newline='', encoding='utf-8') as output:
            writer = csv.writer(output)
            for x in with_year_list: writer.writerow(x)


def main():
    try:
        if len(sys.argv) >= 2: input_file = sys.argv[1]
        else: input_file = input("Please enter input csv file name:")
        if len(sys.argv) >= 3: output_file = sys.argv[2]
        else: output_file = input("Please enter output csv file name:")
        person_birthday_from_wiki(input_file, output_file)
        print("Successfuly created '" + output_file + "-.csv' from '" + input_file + ".csv'.", '\n')
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
                     ' No files with given input/output name are currently open.')

if __name__ == '__main__':
    main()