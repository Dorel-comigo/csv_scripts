import sys, csv, random
from formatted_string import piped_string_to_list
from youtube_videos import youtube_search
from googleapiclient import errors

'''
@Date: 7.6.18
@Version: 1.3.2
@Author: Dorel Moran

@Description: Takes a .csv file as input (comma-delimited) with columns of info for movies/shows/people (title/type/year).
Outputs a .csv file with number of youtube videos for each movie/show/person.

Can manually change in the code the in/output column names, # of videos per item, search query.

@Known Bugs: Sometimes returs "#NAME?" as video id.

'''

def get_videos_youtube(input_file, output_file):
    with open(input_file + '.csv', newline='', encoding='utf-8') as input:
        reader = csv.DictReader(input)
        item_list = []
        for row in reader:
            '''
            Change the input column names and # here.
            If changing # of columns- another change should be made later in the code.
            '''
            item_list.append([row['\ufefftitle'], row['type'], row['year'], row['wiki-en']])

        '''
        Change the output column names and # here.
        If changing # of columns- another change should be made later in the code.
        '''
        video_id_list = [('Name', 'Type', 'Year', 'Wiki', 'VideoID')]
        count = 1
        error_list = []
        for item in item_list:
            try:
                '''
                Change the search query here. 
                '''
                search = youtube_search("'" + item[0] +  " " + item[1] + "'")
                videos = search[1]
                rand = random.sample(range(10), 8)
                try:
                     for i in range(8):
                         video_id_list.append((item[0], item[1], item[2], item[3], videos[rand[int(i)]]['id']['videoId']))
                except IndexError: print('IndexError occured when adding item ', item[0], '.')

                token = ''
                videos_unrelated = []
                for i in range(3):   # Will finally get videos from page 3. (To try getting unrelated videos)
                    search_unrelated = youtube_search("'" + item[0].split(' ', 1)[0] + "'", token = token)
                    token = search_unrelated[0]
                    videos_unrelated = search_unrelated[1]
                video_id_list.append((item[0], item[1], item[2], item[3], videos_unrelated[0]['id']['videoId']))
                video_id_list.append((item[0], item[1], item[2], item[3], videos_unrelated[1]['id']['videoId']))
                print('Latest videos for: ', item[0])
                print('Count: ', count, '\n')
                count = count + 1
            except errors.HttpError:
                print('HttpError occured with: ', item[0])
                error_list.append(item[0])

        print(video_id_list)
        print("error list: ", error_list)

        with open(output_file + '.csv', 'w', newline='', encoding='utf-8') as output:
            writer = csv.writer(output)
            writer.writerows(video_id_list)


# https://www.youtube.com/watch?v=###videoid


def main():
    try:
        if len(sys.argv) >= 2: input_file = sys.argv[1]
        else: input_file = input("Please enter input csv file name:")
        if len(sys.argv) >= 3: output_file = sys.argv[2]
        else: output_file = input("Please enter output csv file name:")
        get_videos_youtube(input_file, output_file)
        print("\nSuccessfuly created '" + output_file + "' from '" + input_file + "'.", '\n')
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n '
              'B. No files with given input/output name are currently open.')
        exit(1)
if __name__ == '__main__':
        main()
