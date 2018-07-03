import sys, csv
from xml.etree import ElementTree

'''
@Date: 17.5.18
@Version: 1.0.2
@Author: Dorel Moran

@Description: Takes an xml file as input and outputs a csv with wanted items.

'''



def xml_items(input_xml, output_csv):
    with open(input_xml + '.xml', 'r', encoding='iso-8859-1') as in1:
        with open(output_csv + '.csv', 'w', newline='', encoding='iso-8859-1') as out1:
            xml = in1.read()
            writer = csv.writer(out1)
            root = ElementTree.fromstring(xml)
            i = 0
            movies_done = False
            shows_done = False
            movie_list = [['name', 'type', 'year']]
            show_list = [['name', 'type', 'year']]
            while movies_done == False or shows_done == False:
                name = root[0][i][0][2][0].text.encode('iso-8859-1').decode('utf-8')
                type = root[0][i][0][0].text.encode('iso-8859-1').decode('utf-8')
                year = root[0][i][1][1][0].text.encode('iso-8859-1').decode('utf-8')
                if root[0][i][0][0].text == 'Movie' and movies_done == False:
                    movie_list.append([name, type, year])
                    if len(movie_list) > 50: movies_done = True
                    print('last addition to list:', movie_list[-1])
                elif root[0][i][0][0].text == 'Series' and shows_done == False:
                    show_list.append([name, type, year])
                    if len(show_list) > 50: shows_done = True
                    print('last addition to list:', show_list[-1])
                i = i + 1
            writer.writerows(movie_list)
            writer.writerows(show_list)


def main():
    try:
        if len(sys.argv) >= 2: input_xml = sys.argv[1]
        else: input_xml = input("Please enter input xml file name:")
        if len(sys.argv) >= 3: output_csv = sys.argv[2]
        else: output_csv = input("Please enter output csv file name:")
        xml_items(input_xml, output_csv)
        print("\nSuccessfuly created '" + output_csv + "'.csv from '" + input_xml + "'.", '\n')
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
              ' No files with given input/output name are currently open.')

if __name__ == '__main__':
        main()