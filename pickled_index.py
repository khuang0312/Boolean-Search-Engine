from os import walk, remove
from os.path import getsize
import json
import pickle
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
import re
from sys import argv, getsizeof
from sortedcontainers import SortedDict

'''
Dictionary of tokens mapped to list of tuples (id, raw_frequency)
'''
def page_text(filepath: str):
    page_text = ""
    with open(filepath) as f:
        html_doc = json.load(f)
        soup = BeautifulSoup(html_doc['content'], "html.parser")
        page_text = soup.get_text()
    return page_text

def get_words(text : str) -> {str : int}:
    '''Uses very simplified rules to get words from the file
        Only lowercase alphanumeric characters

        According to general specifications, we use
        all alphanumeric sequences

        We consider stop words...
    '''
    word_frequencies = {}
    ps = PorterStemmer()
    for word in re.finditer(r'([a-zA-Z0-9]+)', text):
        try:
            word = ps.stem(word.group(0).lower())
        except IndexError:
            print("Something happened with term {}".format(word))
        else:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
 
    return word_frequencies

def write_file(file_name : str, obj):
    '''Wrapper for writing to file
    '''
    with open(file_name, "wb") as f:
        pickle.dump(obj, f)

def load_file(file_name : str):
    '''Wrapper for loading a file
    '''
    obj = None
    with open(file_name, "rb") as f:
        obj = pickle.load(f, encoding="UTF-8")
    return obj

def remove_file(file_path: str):
    try:
        remove(file_path)
    except FileNotFoundError:
        print("File at {} not found.".format(file_path))

if __name__ == "__main__":
    remove_file("index.bin")
    remove_file("doc.bin")
    remove_file("report.txt")
    
    doc_id = 0
    index = {}
    docs  = []
    
    unique_tokens = 0 # probably can't be used anymore
    for domain, dir, pages in walk("DEV/"):
        for page in pages:
            doc_id += 1
            print("Parsing doc {}, Unique Tokens: {}".format(doc_id, unique_tokens)) # DEBUG statement
            
            doc_path = domain + "/" + page
            docs.append(page)

            tokens = get_words(page_text(doc_path))
            for t in tokens:
                if t not in index:
                    index[t] = []
                    unique_tokens += 1 # might have to remove eventually
                index[t].append((doc_id, tokens[t]))
            
   
    print("Done.")
    write_file("index.bin", index)
    write_file("doc.bin", docs)

    with open("report.txt", "w") as f:
        f.write("Kevin Huang, 45279539\n")
        f.write("Klim Rayskiy, 5368211\n")
        f.write("Cedric Lim, 24026891\n")
        f.write("Camille Padua, 42962688\n")
        f.write("Documents parsed: {}\n".format(doc_id))
        f.write("Unique tokens: {}\n".format(unique_tokens))
        f.write("Size of index: {} B\n".format(getsize("index.bin")))
        f.write("Size of index: {} KB\n".format(getsize("index.bin") / 1000 ))
        f.write("Size of index: {} MB\n".format(getsize("index.bin") / 1000000))
