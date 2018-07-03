import sys, codecs, csv, requests, re
from urllib.parse import quote


def clean_res(res):
    # make sure cmp lower case + removing any url parmeters such as 'https://twitter.com/JoeMantegna?lang=en'
    a = []
    for s in res:
        t = s.lower().split('?')[0]
        if 'none.com' in t: t = 'No Match'
        a.append(t)

    return a


def get_majority(res):
    num_of_items = len(res)

    if num_of_items == 1:
        return 'Inconclusive'
    elif num_of_items == 2:
        if res[0] == res[1]:
            return res[0]
        else:
            return 'Inconclusive'
    else:  # num_of_items >= 3
        pot_res = max(res, key=res.count)
        if min(res, key=res.count) == pot_res:
            # either all result are the same or all are different (ignore draw in case > 3 results)
            if res[0] == res[1]:
                return res[0]
            else:
                return 'Inconclusive'
        else:
            return pot_res


# need to add writing of tupples - (worker_id, result)
def get_res(f_in):
    with codecs.open(f_in, "r", encoding="utf-8") as fin:
        r = csv.reader(fin)

        # get 'input name' and 'answer' indexes
        first_line = next(r)
        i, j = first_line.index('Input.name'), first_line.index('Answer.web_url')

        db = {}
        for row in r:
            name, url = row[i], row[j]
            if name not in db:
                db[name] = [url]
            else:
                db[name].append(url)

        res_db = {}
        for key, item in db.items():
            res_db[key] = get_majority(clean_res(item))

    return res_db


def read_file_into_db(db_file):
    with codecs.open(db_file, "r", encoding="utf-8") as f_db:
        db_reader = csv.reader(f_db)
        db = {}
        for row in db_reader:
            db[row[0]] = row[1]

    return db


def write_db_to_file(fout, db):
    with codecs.open(fout, "w", encoding="utf-8") as f_db:
        w = csv.writer(f_db, lineterminator='\n')
        w.writerows(sorted(db.items()))

    return


def add_tags_to_db(new_dic, db, filename):
    for k, v in new_dic.items():
        if k in db and v not in db[k]:
            print('Need to resolve:')
            print(k, db[k], v)
            db[k] = [''.join(c for c in db[k] if c not in '"'), v]
        if k not in db:
            db[k] = [v]

    write_db_to_file(sys.argv[2], db)
    return


def add_mturk_res_to_db():
    if len(sys.argv) != 3:
        print('')
        print('usage: ' + sys.argv[0] + ' <Input - MTurk result file> <DB file>\n')
        print(
            'Script will read DB from file and update it with the results of the MTurk file, re-writing it under the same file name.')
        print('In the process DB will be copied aside for backup.\n')  # TODO
        sys.exit(1)

    # get results from MTurk CSV
    mturk_dic = get_res(sys.argv[1])

    # read db
    db = read_file_into_db(sys.argv[2])

    add_tags_to_db(mturk_dic, db, sys.argv[2])

    return


def fb_id_finder(target_url):
    result = requests.get(target_url)

    if result.ok:
        # print(len(result.text), len(result.content), result.text==result.content)
        result = result.text
        profile_id = re.search(r'profile_id=[0-9]+', result)
        if not profile_id: profile_id = re.search(r'page_id=[0-9]+', result)
        if not profile_id: profile_id = re.search(r'"pageID":"[0-9]+"', result)
        if profile_id:
            profile_id = re.search(r"[0-9]+", profile_id.group()).group()
        else:
            'permission denied'
            return None
        return profile_id
    else:
        return None


def clean(s):
    return '{}'.format(''.join(c for c in s if c not in '"')[1:-1])


def add_fb_id_to_db():
    if len(sys.argv) != 2:
        print('')
        print('usage: ' + sys.argv[0] + ' <DB FB file>\n')
        print('Find FB ID per each facebook url value in db.')
        print('In the process DB will be copied aside for backup.\n')  # TODO
        sys.exit(1)

    # read db
    db = read_file_into_db(sys.argv[1])

    for k, v in db.items():
        v = v[2:-2].strip()
        if v.find('No Match') < 0 and v.find('conclusi') < 0:
            print('requesting url: %s' % v)

            a = re.search(r'-[0-9]+', v)
            if a:
                fbid = a.group()[1:]
            else:
                fbid = fb_id_finder(v)

            if fbid is not None:
                print(fbid)
                db[k] = (clean(db[k]), fbid)
            else:
                print(k, v)
        else:
            db[k] = (clean(db[k]), 0)

    write_db_to_file(sys.argv[1], db)

    return


def main():
    add_mturk_res_to_db()
    # add_fb_id_to_db()

    return


if __name__ == '__main__':
    main()
