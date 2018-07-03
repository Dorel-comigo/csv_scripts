import sys, requests, json, csv
from itertools import cycle

'''
@Date: 18.5.18
@Version: 1.0.1
@Author: Dorel Moran

@Description: Gets informative items from TMDB discover API feature. 
Roundrobin for keys in case one key is blocked.
Sorting is changeable in the code.
Takes as input: A. csv output file name.  B. type of item- movie or tv show.  C. # of pages of TMDB discover. 
Output: csv file with 6 columns- 'name', 'year', 'type', 'vote count', 'vote average','popualrity'.

Notice: Every page is 20 items.

'''

TMDB_API_KEYS = ['1cd4c5461b83c3b886ace8005facd7d0', '6e8e7e949bcf4e82a3dbae0849cef39a',
                 'df910e6ce2f2db1b5314b3bf5e7bbbd3', 'ea133a1262edfd4b0544162485137ad6',
                 'd7baf4399b513eea64d8ffa566e432af', 'eac77b95b2766ead0b4993b653fda64f',
                 'fa70cd566549920f1d62c63e63b5dad8', '457749981a7dcb9c779a0ac033473536',
                 '747a6e415994f0543ece1ada3a6e1d85', '60238956bbe9c8f5bfb96b414f6acec8']

def get_items(output_file, type, pages):
    items = [['name', 'type', 'year', 'vote_count', 'vote_average', 'popularity']]
    key_pool = cycle(TMDB_API_KEYS)
    current_key = next(key_pool)
    attempt = 1
    with open(output_file + '.csv', "w", encoding="utf-8") as f_db:
        w = csv.writer(f_db, lineterminator='\n')
        for i in range(0, int(pages)):
            repeat = True
            while repeat == True:
                try:
                    '''
                    To change sort- change text after 'sort_by='. Options: 'title' , 'year'. 
                    Add '.desc' or '.asc' for descending or ascending.
                    '''
                    response = requests.get('https://api.themoviedb.org/3/discover/' +
                               type + '?sort_by=year.asc&page=' + str(i + 1) + '&api_key=' + current_key)
                    if response.ok:
                        res = json.loads(response.text)
                        print('\nAttempt ' + str(attempt) + '. Page ' + str(i + 1) + '.')
                        for result in res['results']:
                            if not result:
                                continue
                            '''
                            Gives results only if the movie / show is from that language.
                            '''
                            if result['original_language'] == 'es':
                                if type == 'tv':
                                    items.append((result.get('name'), 'show', result['first_air_date'][0:4],
                                                  result['vote_count'], result['vote_average'], result['popularity']))
                                    w.writerow(items[-1])
                                elif type == 'movie':
                                    items.append((result.get('title'), 'movie', result['release_date'][0:4],
                                                  result['vote_count'], result['vote_average'], result['popularity']))
                                    w.writerow(items[-1])
                                print('last item added:' , items[-1])
                            else: pass
                        current_key = next(key_pool)
                        repeat = False
                    else:
                        print('Attempt ' + attempt + ' failed. Response not OK with key: ' + current_key)
                        current_key = next(key_pool)
                    attempt = attempt + 1
                except requests.exceptions.ConnectionError:
                            print('\n### Connection error. Attempting again.')
                            current_key = next(key_pool)
        print('\nWriting complete.')


def main():
    try:
        if len(sys.argv) >= 2: output_file = sys.argv[1]
        else: output_file = input("Please enter output csv file name:")
        if len(sys.argv) >= 3: type = sys.argv[2]
        else: type = input("\nEnter 'movie' for movies or 'tv' for tv shows:")
        if (type == 'movie' or type == 'tv'): pass
        else:
            print("\nWrong input. Enter 'movie' or 'tv'.")
            exit(1)
        if len(sys.argv) >= 4: pages = sys.argv[3]
        else: pages = input("\nEnter # of pages:")
        if pages.isdigit: pass
        else:
            print("\nWrong input. Enter a number.")
            exit(1)
        get_items(output_file, type, pages)
        print("\nSuccessfuly created '" + output_file + "'.\n")
    except IOError:
        print('I\O Error - make sure: \n A. Name of input file is correct. '
              '\n B. No files with given input/output name are currently open.')
        exit(1)

if __name__ == '__main__':
    main()

