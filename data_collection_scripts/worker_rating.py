import csv, sys
from formatted_string import formatted_url

'''
@Date: 23.5.18
@Version: 1.1.2
@Author: Dorel Moran

@Description: Take 2 csv's as input:
A. The ouput csv from mturk website as results.
B. The corresponding compressed results csv, created from the 'compressed_results.py' python file.
From A- make a list of tuples of (worker ID, input name, answer).
Compare with B's tuples of (input name, answer) for reference for 'correct' / 'wrong' answers.

outputs a csv with worker ID , % of correct answers, number of correct answers, and total answers.



'''

def worker_rating(input_A, input_B, output_file):
    with open(input_A + '.csv', newline='', encoding='utf-8') as in_A:
        with open(input_B + '.csv', newline='', encoding='utf-8') as in_B:
            reader_A = csv.DictReader(in_A)
            reader_B = csv.DictReader(in_B)

            '''
            Change column names to relevant ones from the result.csv file. 
            The 3 columns should always be: 
            A worker ID column, a query column (the question we asked), and an answer column.
            '''
            worker_answers = []
            for row in reader_A: worker_answers.append([row['WorkerId'], row['HITId'], formatted_url(row['Answer.category'])])
            #for row in reader_A: worker_answers.append([row['WorkerId'], row['HITId'], formatted_url(row['Answer.match'])])

            '''
            Change column names to relevant ones from the compressed_result.csv file (which uses majority rules).
            The 2 columns should always be:
            A query column (the question we asked) and an answer column (which is the majority answer).
            '''
            majority_answers = []
            for row in reader_B: majority_answers.append([row['HITId'], formatted_url(row['answer_tag'])])
            #for row in reader_B: majority_answers.append([row['HITId'], formatted_url(row['answer_match'])])

            worker_grades = {}  # Tuples of [workerID, % correct, correct answers, total answers]

            for maj_ans in majority_answers:
                for worker_ans in worker_answers:
                    if maj_ans[0] == worker_ans[1]:
                        answered = 0
                        correct = 0
                        if worker_ans[0] in worker_grades:
                            answered = worker_grades[worker_ans[0]][2]
                            correct = worker_grades[worker_ans[0]][1]
                        answered = answered + 1
                        if maj_ans[1] == worker_ans[2]: correct = correct + 1
                        percents = str(round(((correct / answered) * 100), 2)) + '%'
                        worker_grades[worker_ans[0]] = [percents, correct, answered]


            with open(output_file + '.csv', 'w', newline='', encoding='utf-8') as out:
                writer = csv.writer(out)
                writer.writerow(['worker ID', '% correct', 'correct answers', 'total answers'])
                for key, value in worker_grades.items(): writer.writerow([key, value[0], value[1], value[2]])


def main():
    try:
        if len(sys.argv) >= 2: input_A = sys.argv[1]
        else: input_A = input("Please enter mturk result input csv file name:")
        if len(sys.argv) >= 3: input_B = sys.argv[2]
        else: input_B = input("Please enter compressed result input csv file name:")
        if len(sys.argv) >= 4: output_file = sys.argv[3]
        else: output_file = input("Please enter output csv file name:")
        worker_rating(input_A, input_B, output_file)
        print("\nSuccessfuly created '" + output_file + "' from '" + input_A + "' and '" + input_B + "'.", '\n')
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
              ' No files with given input/output name are currently open.')
        exit(1)
if __name__ == '__main__':
        main()
