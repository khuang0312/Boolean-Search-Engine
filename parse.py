# This module is dedicated to the processing of webpages
# Webpages in this context are the JSON files in the "DEV/" folder

from bs4 import BeautifulSoup
import json
import re

def page_text(filepath : str) -> str:
    '''Returns the readable text of a webpage 

       Warning: the string is not printable because of Unicode characters
       within it...

       We need to also consider bolding (b, strong) and headings (h1, h2, h3)
    '''
    page_text = ""

    with open(filepath) as f:
        html_doc = json.load(f)
        soup = BeautifulSoup(html_doc['content'], "html.parser")
        page_text = soup.get_text()

    return page_text

def get_words(text : str) -> (int, {str : int}):
    '''Uses very simplified rules to get words from the file
        Only lowercase alphanumeric characters

        According to general specifications, we use
        all alphanumeric sequences

        We consider stop words...
    '''
    words_found = 0
    word_frequencies = {}
    
    for word in re.finditer(r'([a-zA-Z0-9]+)', text):
        word = word.group(0).lower()
        if word not in word_frequencies:
            words_found += 1
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1
 
    return words_found, word_frequencies


def write_json(name : str, initial_obj):
    '''Creates or overwites a json file of a specified name with a
        specific json-serializable object...
    '''
    with open(name + ".json", 'w') as json_file:
        json.dump(initial_obj, json_file)

def load_json(name : str) -> dict:
    '''Gets a JSON object from a file
    '''
    mapping = {}
    with open(name + ".json", "r") as json_file:
        mapping = json.load(json_file)
    return mapping

def append_json(name : str, initial_obj):
    '''Creates or appends to a json file of a specified name with a
        specific json-serializable object...
    '''
    with open(name + ".json", 'a') as json_file:
        json.dump(initial_obj, json_file)

def merge_index(name1: str, name2: str) -> {str : [{str : int, str: int}]}:
    '''Takes the keys in name2 that are also in key one and adds the values
        to the corresponding keys in key2

        For example {"apple" : [{'a' : 2}]}, {"apple" : [{'b' : 2}]}
        {"apple" : [{'a': 2}, {'b' : 2}]}i
    '''
    index1 = load_json(name1)
    index2 = load_json(name2)
    
    keys_to_purge = set()

    for token in index2.copy():
        if token in index1:
            index1[token] += index2[token]
            keys_to_purge.add(token)

    for key in keys_to_purge:
        del index2[key]

    write_json(name1, index1)
    write_json(name2, index2)

def merge_indices(root_name: str, batches : int):
    '''
    '''
    pass
    # for i in range(batches - 1):
    #    for j in range(i + 1, batches):
    #        merge_index(root_nane + str(i), )



if __name__ == "__main__":
    print(get_words(page_text("DEV/aiclub_ics_uci_edu/8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json")))
