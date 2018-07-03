import sys
import codecs
import csv
from urllib.parse import quote

def clean_quotes(s):
    return ''.join(c for c in s if c not in '"')

def add_url(filename, new_filename, url):

    with codecs.open(filename,'r', encoding='utf-8') as csvinput:
        with codecs.open(new_filename, 'w', encoding='utf-8') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)

            a = []
            #row = next(reader)
            #row.append('search')
            #a.append(row)
            a.append(['name', 'search'])

            url = clean_quotes(url)
                  
            for row in reader:
                if row:     # TODO: need to handle Names that has comma inside - e.g.: "Cuba Gouding, Jr."
                    row.append(url + quote('"{}"'.format(clean_quotes(row[0]))))
                    a.append(row)

            writer.writerows(a)
    
    return


def main():
    
    if len(sys.argv) != 4:
        print ('\nUsage: ' + sys.argv[0] + ' <input file> <output file> <search URL>\n\n')
        print ('E.g.: ' + sys.argv[0] + ' input.csv out.csv "https://twitter.com/search?f=users&q="\n\n')
        sys.exit(1)

    add_url(sys.argv[1], sys.argv[2], sys.argv[3])



if __name__ == '__main__':
    main()

