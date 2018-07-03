import sys, requests, json, csv
from itertools import cycle

'''
@Date: 26.4.18
@Version: 1.0.0
@Author: Dorel Moran

@Description: Takes as input a csv file seperated by pipes where first 3 "columns" (by pipes) are: name|type|year.
Goes over each item in the list with a roundrobin of TMDB keys and proxies to send a request to TMDB's API and
returns a popularity real numnber for each item.

Outputs a .csv file with same number of piped columns as in the input csv plus a piped column of popularity.

Notice that the code counts first line as a valid item, if the input file has a header- un-comment the relevant lines.

'''


TMDB_API_KEYS = ['1cd4c5461b83c3b886ace8005facd7d0', '6e8e7e949bcf4e82a3dbae0849cef39a',
                 'df910e6ce2f2db1b5314b3bf5e7bbbd3', 'ea133a1262edfd4b0544162485137ad6',
                 'd7baf4399b513eea64d8ffa566e432af', 'eac77b95b2766ead0b4993b653fda64f',
                 'fa70cd566549920f1d62c63e63b5dad8', '457749981a7dcb9c779a0ac033473536',
                 '747a6e415994f0543ece1ada3a6e1d85', '60238956bbe9c8f5bfb96b414f6acec8']

PROXIES = ['159.65.0.210:3128', '145.249.106.107:8118', '89.236.17.106:3128',
           '92.53.73.138:8118', '85.187.245.51:53281', '42.104.84.106:8080',
           '218.166.132.236:8088', '92.222.79.39:8181', '52.164.249.198:3128',
           '35.169.210.105:3389',]

def get_popularity(input_file, output_file):
    with open(input_file + '.csv', newline='', encoding='utf-8') as input:
        reader = csv.reader(input)
        #header = reader.__next__()  commented since first row isn't repeat header
        items_list = []
        for row in reader:
            items_list.append(((row[0].split('|')[0]), row[0].split('|')[1] , row[0].split('|')[2]))
        i = 0
        for x in items_list:
            b = list(x)
            if b[1] == 'film': b[1] = 'movie?'
            else: b[1] = 'tv?'
            b[0] = b[0].replace(' ', '+')
            items_list[i] = b
            i = i + 1
        # Now got tuples of (title, type, year) suited for an API search

        name_popularity_list = []
        key_pool = cycle(TMDB_API_KEYS)
        proxy_pool = cycle(PROXIES)
        current_key = next(key_pool)
        current_proxy = next(proxy_pool)
        count = 1
        for i in range(1,2):
            for item in items_list:
                repeat = True
                while repeat == True:
                    try:
                        response = requests.get('https://api.themoviedb.org/3/search/' + item[1] + 'query="' + item[0] +
                                            '&year=' + item[2] + '"&page=' + str(i) + '&api_key=' + current_key,
                                            proxies = {'http': current_proxy, 'https': current_proxy})
                        if response.ok:
                            print('Count: ', count, '\nKey: ', current_key, '\nProxy: ', current_proxy, '\nResponse- ok.')
                            res = json.loads(response.text)
                            if item[1] == 'movie?':
                                name_popularity_list.append(
                                    (res['results'][0].get('title'), res['results'][0]['popularity']))
                            else:
                                name_popularity_list.append(
                                    (res['results'][0].get('original_name'), res['results'][0]['popularity']))
                            print("Added to 'name & popularity' list: ", name_popularity_list[-1], '\n')
                            current_key = next(key_pool)
                            current_proxy = next(proxy_pool)
                            count = count + 1
                        else: print('Response not OK with key: ' + current_key)
                        repeat = False
                    except requests.exceptions.ConnectionError:
                        print('\n### Connection error with the proxy: ', current_proxy, ' ###\n')
                        current_proxy = next(proxy_pool)
        popularity_list = []
        for x in name_popularity_list: popularity_list.append(x[1])

        #print to csv
        with open(output_file + '.csv', 'w', encoding='utf-8') as output:
            writer = csv.writer(output, lineterminator='\n')
            all = []
            input.seek(0)
            '''   commented since there's no header
            row = next(reader)
            row.append('popularity')
            all.append(row)
            '''
            i = 0
            count = 1
            for row in reader:
                all.append(row[0] + '|' + str(popularity_list[i]))
                print('\nCount=', count)
                print('Added to csv writer: ', all[-1])
                if i < len(popularity_list): i = i + 1
                else: break
                count = count + 1
            for x in all:
                writer.writerow([x])
            print('\nWriting complete.')



def main():
    try:
        if len(sys.argv) >= 2: input_file = sys.argv[1]
        else: input_file = input("Please enter input csv file name:")
        if len(sys.argv) >= 3: output_file = sys.argv[2]
        else: output_file = input("Please enter output csv file name:")
        get_popularity(input_file, output_file)
        print("\nSuccessfuly created '" + output_file + "' from '" + input_file + "'.", '\n')
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B. No files with given input/output name are currently open.')
        exit(1)
if __name__ == '__main__':
        main()
else:
    print("Using 'get_popularity_tmdb.py' method:", '\n')
    main()
