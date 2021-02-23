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
def page_text(filepath: str) -> (str, str):
    ''' Returns the page text and URL from the given JSON filename,
        in the following format (page_text, URL)
    '''
    page_text = ""
    url = ""
    with open(filepath) as f:
        html_doc = json.load(f)
        soup = BeautifulSoup(html_doc['content'], "html.parser")
        page_text = soup.get_text()
        url = html_doc["url"]
    return (page_text, url)

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

# given a query, see if we have it on the dictionary structure
def contains_query(query : str, word_dict : dict) -> bool :
    query = query.lower()
    lst_words = query.split("and")
    for word in lst_words:
        if word not in word_dict: 
            return False
    return True

def write_bin(file_name : str, obj):
    '''Wrapper for writing to file
    '''
    with open(file_name, "wb") as f:
        pickle.dump(obj, f)

def load_bin(file_name : str):
    '''Wrapper for loading a file
    '''
    obj = None
    with open(file_name, "rb") as f:
        obj = pickle.load(f, encoding="UTF-8")
    return obj

def write_file(file_name : str, text : str):
    '''Wrapper for writing to file
    '''
    with open(file_name, "w") as f:
        # pickle.dump(obj, f)
        f.write(text)

def load_file(file_name : str):
    '''Wrapper for loading a file
    '''
    obj = None
    with open(file_name, "r") as f:
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
    remove_file("url.bin")
    
    doc_id = 0
    index = {}
    docs  = []
    urls = []
    
    unique_tokens = 0 # probably can't be used anymore
    for domain, dir, pages in walk("DEV/"):
        for page in pages:
            # doc_id += 1
            print("Parsing doc {}, Unique Tokens: {}".format(doc_id, unique_tokens)) # DEBUG statement
            
            doc_path = domain + "/" + page
            page_data = page_text(doc_path)

            docs.append(page)
            urls.append(page_data[1])

            tokens = get_words(page_data[0])

            for t in tokens:
                if t not in index:
                    index[t] = []
                    unique_tokens += 1 # might have to remove eventually
                index[t].append((doc_id, tokens[t]))
            
            doc_id += 1
            
   
    print("Done.")
    write_bin("index.bin", index)
    write_bin("doc.bin", docs)
    write_bin("url.bin", urls)

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
