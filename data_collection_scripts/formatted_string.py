import re

'''
@Date: 3.5.18
@Version: 1.3.0
@Author: Dorel Moran

@Description: Formats strings for SQL usage, mturk usage, etc.

'''

def formatted_url(url):
    result = url.lower()
    #if 'none' in result:
        #result = 'no match'
    if '?lang=en' in result:
        result = result.split('?lang=en')[0]
    if 'http:' in result:
        result = result.replace('http:', 'https:')
    return result


def formatted_name(name):
    result = name.lower()
    result = result.replace(' ', '_')
    result = result.replace('-', '_')
    result = result.replace(' & ', '_and_')
    result = re.sub(r'[\W]+', '', result)
    return result


def piped_string_to_list(piped_string):
    result = []
    i = 0
    while i <= piped_string.count('|'):
        result.append(piped_string.split('|')[i])
        i = i + 1
    return result


def piped_list_to_lists(piped_list):
    result = []
    for piped_string in piped_list: result.append(piped_string_to_list(piped_string))
    return result


def list_to_piped_string(list_input):
    result = ''
    for item in list_input: result = result + item + '|'
    return result[:-1]


def lists_to_piped_list(list_input):
    result = []
    for item in list_input: result.append(list_to_piped_string(item))
    return result


