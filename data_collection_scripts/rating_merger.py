import csv, sys
from formatted_string import formatted_url

'''
@Date: 5.6.18
@Version: 1.3.0
@Author: Dorel Moran

@Description: Takes 2 worker_rating csv files as input and merges them into one worker_rating csv file that contains both.
In the case of 1 wortker in both input files- the merge method will output a correct merged statistics for him.

'''


def rating_merger(input_A, input_B, output_file):
    with open(input_A + '.csv', newline='', encoding='utf-8') as in_A:
        with open(input_B + '.csv', newline='', encoding='utf-8') as in_B:
            reader_A = csv.reader(in_A)
            reader_B = csv.reader(in_B)
            reader_A.__next__()
            reader_B.__next__()
            ratings1 = {}
            rating_values1 = []
            ratings2 = {}
            rating_values2 = []
            for row in reader_A:
                rating_values1.append([row[1], row[2], row[3]])
                ratings1[row[0]] = rating_values1[-1]
            for row in reader_B:
                rating_values2.append([row[1], row[2], row[3]])
                ratings2[row[0]] = rating_values2[-1]

            # Merging process.
            new_workers = {}
            changed_workers = {}
            for key, value in ratings2.items():
                if key in ratings1: # If the worker is already in the first csv.
                    ratings1[key][1] = int(ratings1[key][1]) + int(value[1])
                    ratings1[key][2] = int(ratings1[key][2]) + int(value[2])
                    before_percent = float(ratings1[key][0].replace('%', ''))
                    ratings1[key][0] = str(round(((ratings1[key][1] / ratings1[key][2]) * 100), 2)) + '%'
                    after_percent = float(ratings1[key][0].replace('%', ''))

                    # This part is for showing what changed in which worker.
                    changed_values = []
                    if after_percent > before_percent:
                        changed_values.append(ratings1[key][0] + '(+' + str(round((after_percent - before_percent), 2)) + '%)')
                    elif after_percent < before_percent:
                        changed_values.append(ratings1[key][0] + '(-' + str(round((before_percent - after_percent), 2)) + '%)')
                    else: changed_values.append(ratings1[key][0] + '(+0.00%)')
                    if int(ratings1[key][1]) < int(value[1]) + int(ratings1[key][1]):
                        changed_values.append(str(ratings1[key][1]) + '(' + '+'  + value[1] + ')')
                    else: changed_values.append(str(ratings1[key][1]) + '(+0)')
                    changed_values.append(str(ratings1[key][2]) + '(+' + value[2] + ')')
                    changed_workers[key] = changed_values

                else:   # If the worker is new.
                    ratings1[key] = value
                    new_workers[key] = value


            # Writing process.
            with open(output_file + '.csv', 'w', newline='', encoding='utf-8') as out:
                writer = csv.writer(out)
                writer.writerow(['worker ID', '% correct', 'correct answers', 'total answers'])
                for key, value in ratings1.items(): writer.writerow([key, value[0], value[1], value[2]])
            with open(output_file + '_updated-workers.csv', 'w', newline='', encoding='utf-8') as out2:
                writer2 = csv.writer(out2)
                writer2.writerow(["Workers that got updated:"])
                writer2.writerow([])
                for key, value in changed_workers.items(): writer2.writerow([key, str(value[0]), str(value[1]),
                                                str(value[2]), 'https://requester.mturk.com/workers/' + key])
                writer2.writerow([])
                writer2.writerow(["New workers:"])
                for key, value in new_workers.items(): writer2.writerow([key, str(value[0]), str(value[1]),
                                                str(value[2]), 'https://requester.mturk.com/workers/' + key])


def main():
    try:
        if len(sys.argv) >= 2:
            input_A = sys.argv[1]
        else:
            input_A = input("Please enter the file name of the rating csv file that will get updated:")
        if len(sys.argv) >= 3:
            input_B = sys.argv[2]
        else:
            input_B = input("Please enter the file name of the rating csv file that will update the first:")
        if len(sys.argv) >= 4:
            output_file = sys.argv[3]
        else:
            output_file = input("Please enter output csv file name:")
        rating_merger(input_A, input_B, output_file)
        print("\nSuccessfuly created '" + output_file + ".csv' and '" + output_file + "_updated-workers.csv'.", '\n')
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
              ' No files with given input/output name are currently open.')
        exit(1)


if __name__ == '__main__':
    main()
