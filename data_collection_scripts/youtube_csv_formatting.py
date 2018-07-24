import csv, sys

def youtube_csv_formatting(input_csv):
    with open(input_csv, newline='', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        row_list = [[row['name'],row['type'],row['year'],row['video_id'],row['relation']] for row in reader]
        for row in row_list: print(row)
        csv_file.seek(0)
        reader.__next__()
        name_list = [row['name'] for row in reader]
        name_set = set(name_list)

        new_list = []
        for name in name_list:
            for row in row_list:
                if row[0] == name:
                    if row[0] in [i[0] for i in new_list]:
                        temp = row[]
                    temp = row
                    new_list.append(row)




def main():
    input_csv = sys.argv[1]
    youtube_csv_formatting(input_csv)

if __name__ == '__main__':
    main()