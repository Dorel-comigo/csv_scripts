import csv, sys, re
from formatted_string import list_to_piped_string, lists_to_piped_list

'''
@Date: 24.6.18
@Version: 1.0.0
@Author: Dorel Moran

@Description: 
'''

def annotation_verifier(input_file, output_file):
    with open(input_file + '.csv', encoding='utf-8') as input:
        reader = csv.DictReader(input)
        out_dict= {}
        for row in reader:
            for header, value in     row.items():
                try:
                    out_dict[header].append(value)
                except KeyError:
                    out_dict[header] = [value]

        i = 0
        for machine_tag in out_dict['machine_tag']:
            out_dict['machine_tag'][i] = out_dict['machine_tag'][i].replace('PER', 'person')
            out_dict['machine_tag'][i] = out_dict['machine_tag'][i].replace('ORG', 'organization')
            out_dict['machine_tag'][i] = out_dict['machine_tag'][i].replace('LOC', 'location')
            i += 1

        i = 0
        for answer_tag in out_dict['answer_tag']:
            if answer_tag == 'none':
                out_dict['answer_match'][i] = 'not a name'
            elif answer_tag != out_dict['machine_tag'][i]:
                out_dict['answer_match'][i] = 'wrong type'
            i += 1

        value_list = []
        for key, values in out_dict.items():
            value_list.append(values)
        value_list.pop(0)
        value_list.pop(-1)
        value_list = list(map(list, zip(*value_list)))


        with open(output_file + '.csv', 'w', newline='', encoding='utf-8') as output:
            writer = csv.writer(output)
            writer.writerow(['file_name|line_number|mention|match_type|correct_tag'])
            for x in value_list:
                writer.writerow([list_to_piped_string(x)])
            print("\nSuccessfuly created '" + output_file + ".csv'   from '" + input_file + ".csv'.")




def main():
    try:
        if len(sys.argv) >= 2: input_file = sys.argv[1]
        else: input_file = input("Please enter input file name:")
        #if len(sys.argv) >= 3: output_file = sys.argv[2]
        #else: output_file = input("Please enter output csv file name:")
        output_file = re.sub(r'_.*', '_annotations_v1.0', input_file)
        annotation_verifier(input_file, output_file)
    except IOError:
        print('\nI\O Error - make sure: \n A. Name of input file is correct. \n B.'
              ' No files with given input/output name are currently open.')
        exit(1)
if __name__ == '__main__':
        main()