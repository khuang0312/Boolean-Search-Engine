import sys
import pickle
import re
from nltk.stem import PorterStemmer
import parse
from timer import Timer, to_milliseconds

'''
Queries to test:

cristina lopes
machine learning
ACM
master of software engineering
'''

'''
INDEX DATA STRUCTURE
{token : [(doc_id, )]}
'''


''' 
REGEX PATTERNS

re.split("\W+", "a b      c     ; d") # gets the individual terms, return ['a', 'b', 'c', 'd']

'''

def get_posting(token : str) -> [tuple]:
    ''' Returns the postings of the given token '''
    try:
        return  index[token]
    except KeyError:
        print("Token \'{}\' not found!".format(token))

def get_url_names(postings : [(int, int)]):
    ''' Given the list of postings, return a list of the 
        associated URLs
    '''
    global url
    result = list()
    # print("posting: {}".format(postings))
    for posting in postings:
        ID = posting[0]
        print(ID)
        result.append(url[ID])

    return result


def transform_url(url : str) -> str:
    ''' Removes fragment and adds "/" to the end if it 
        doesn't already have one for consistency
    '''
    url = url[:url.find("#")]
    if not url.endswith("/"):
        url = url + "/"
    return url

def is_valid(url : str) -> str:
    # invalid_file_types = [".ph", ".tx", ".htm", "prog", ".ht"]
    for filetype in invalid_file_types:
        if url.endswith(filetype):
            return False
    return True

if __name__ == "__main__":

    ''' Load in the goods '''
    print("Loading index into memory...")
    url = parse.load_bin("url.bin")
    print("url.bin loaded (len = {})".format(url))
    index = parse.load_bin("index.bin")
    print("Done.")
    # INDEX = open("merged_index.txt")

    ''' Getting query input '''
    t = Timer("timer") 
    while (1):
        query = input("Input query: ")
    
        t.reset(query)
        result = process_query(query)
        t.stop()    # end timer
        print("Search time elapsed: {}ms".format(to_milliseconds(t.time_elapsed())))
        result_urls = get_url_names(result)

        r = 0
        i = 0
        top5 = list()

        while r < 5:
            url = transform_url(result_urls[i])
            url = url[:url.find("#")]

            if url not in top5:
                top5.append(url)
                r += 1
            i += 1
        
        for url in top5:
            print(url)
        print()


    


