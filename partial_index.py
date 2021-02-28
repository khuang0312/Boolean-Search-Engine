from os import walk
from os.path import getsize
import json
import pickle
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
import re
from sys import argv, getsizeof
from sortedcontainers import SortedDict
import parse

'''
Dictionary of tokens mapped to list of lists [doc_id, positions in doc]
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

def get_words(text : str) -> {str : [int]}:
    '''Uses very simplified rules to get words from the file
        Only lowercase alphanumeric characters

        According to general specifications, we use
        all alphanumeric sequences

        We consider stop words...
    '''
    word_frequencies = {}
    ps = PorterStemmer()

    word_pos = 0
    for word in re.finditer(r'([a-zA-Z0-9]+)', text):
        try:
            word = ps.stem(word.group(0).lower())
        except IndexError:
            print("Something happened with term {}".format(word))
        else:
            if word not in word_frequencies:
                word_frequencies[word] = []
            word_frequencies[word].append(word_pos)
            word_pos += 1
 
    return word_frequencies


def write_index(index : 'SortedDict', index_filename : str):
    ''' writes index to text file '''
    
    with open(index_filename, "w") as f:
        for key in index:
            line = "{} {}\n".format(key, index[key])
            f.write(line)

if __name__ == "__main__":
    
    BATCH_SIZE = 5_000_000 # in bytes

    parse.cleanup_files()
    
    STOP = 0
    BREAK = False
    batch_number = 1
    doc_id = 0

    index_index = dict() # key = token, value = file seeking position
    index = SortedDict() # dict - SortedDict()
    docs  = []
    urls = []
    
    unique_tokens = 0 # probably can't be used anymore
    for domain, dir, pages in walk("DEV/"):
        for page in pages:
            print("Parsing doc {}, Unique Tokens: {}, Size of Index {}".format(
                doc_id, unique_tokens, getsizeof(index))) # DEBUG statement
            
            doc_path = domain + "/" + page
            page_data = page_text(doc_path)

            docs.append(page)
            urls.append(page_data[1])

            tokens = get_words(page_data[0])

            for t in tokens:
                if t not in index:
                    index[t] = []
                    unique_tokens += 1 # might have to remove eventually
                index[t].append([doc_id] + tokens[t])            
            doc_id += 1
            

            if getsizeof(index) > BATCH_SIZE:
                
                # write to file
                index_filename = "index" + str(batch_number) + ".txt"
                print("Writing {} to disk...".format(index_filename))
                write_index(index, index_filename)

                # start empty current index, start a new one
                batch_number += 1
                index = SortedDict()

    parse.write_bin("doc.bin", docs)    # maps docID to file names
    parse.write_bin("url.bin", urls)    # maps docID to URLs

    print("Done.")
    
