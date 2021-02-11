# This module is dedicated to the processing of webpages
# Webpages in this context are the JSON files in the "DEV/" folder

from bs4 import BeautifulSoup
import json
import re

def page_text(filepath : str) -> str:
    '''Returns the readable text of a webpage 

       Warning: the string is not printable because of Unicode characters
       within it...
    '''
    page_text = ""

    with open(filepath) as f:
        html_doc = json.load(f)
        soup = BeautifulSoup(html_doc['content'], "html.parser")
        page_text = soup.get_text()

    return page_text

def get_words(text : str) -> (int, {str : int}):
    '''Uses very simplified rules to get words from the file
        Only lowercase sequences of 3+ alphabetic characters
    '''
    words_found = 0
    word_frequencies = {}

    for word in re.finditer(r'([a-zA-Z0-9]{3,})', text):
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
    with open(name, 'w') as json_file:
        json.dump(initial_obj, json_file)

def load_json(name : str) -> dict:
    '''Gets a JSON object from a file
    '''
    mapping = {}
    with open(name, "r") as json_file:
        mapping = json.load(json_file)
    return mapping

if __name__ == "__main__":
    print(get_words(page_text("DEV/aiclub_ics_uci_edu/8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json")))
