from urllib import request, error
import json, sys, csv
import requests

'''
@Date: 31.5.18
@Version: 1.0.0
@Author: Dorel Moran

@Description: 

'''

def youtube_url_tester(input_file, output_file):
    with open(input_file + '.csv', newline='', encoding='utf-8') as input:
        with open(output_file + '.csv', 'w', newline='', encoding='utf-8') as output:
            reader = csv.reader(input)
            reader.__next__()
            writer = csv.writer(output)
            request = ''
            json_data = ''
            bad_list = []
            counter = 1
            for row in reader:
                try:
                    request = requests.get("https://www.googleapis.com/youtube/v3/videos?part=id&id=" + row[4] +
                                              "&key=AIzaSyCr7CEDeND-PtfkTL9QVk0taakQkWOhnZQ")
                    json_data = json.loads(request.text)
                    if  not json_data['items']:
                        print('wrote ', row[0] + '. It doesn\'t exist.')
                        bad_list.append(row)
                    else:
                        print('wrote ', row[0] + '. It exist.')
                    print(counter , '\n')
                    counter = counter + 1
                except error.URLError:
                    print(row[0] + 'not opening')
            print(bad_list)



def main():
    try:
        if len(sys.argv) >= 2: input_file = sys.argv[1]
        else: input_file = input("Please enter input csv file name:")
        if len(sys.argv) >= 3: output_file = sys.argv[2]
        else: output_file = input("Please enter output csv file name:")
        youtube_url_tester(input_file, output_file)
        print("\nSuccessfuly created '" + output_file + "'.csv from '" + input_file + ".csv'.", '\n')
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
              ' No files with given input/output name are currently open.')
if __name__ == '__main__':
        main()