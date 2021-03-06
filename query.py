import sys
import pickle
import re
from nltk.stem import PorterStemmer
import parse
from math import log10, sqrt
from time import perf_counter,time


from collections import OrderedDict

'''
Queries to test:

cristina lopes
machine learning
ACM
master of software engineering
computer science
computers

'''

'''
INDEX DATA STRUCTURE
{token : [(doc_id, )]}
'''

''' 
REGEX PATTERNS

re.split("\W+", "a b      c     ; d") # gets the individual terms, return ['a', 'b', 'c', 'd']

'''


def get_postings(token : str) -> [list]:
    ''' Returns the postings of the given token 
    '''
    try:
        global merged_index
        global index_index
        seek = int(index_index[token])
        merged_index.seek(seek)
        # werner [[30886, 6.258362786994808, 375, 4964, 5000], [30936, 4.236864622317388, 526]]
        line = merged_index.readline()
        return eval(line.split(" ",1)[1])
    except KeyError:
        print("Token \'{}\' not found!".format(token))

def intersect(p1 : list, p2 : list) -> [(int, int)]:
    ''' Given two sorted (by docID) postings lists, merge them 
        together into a single list. 
        Returns list of tuples (docIDs, term freq).
        len(p1) must be less than len(p2).
        Used psudeo code form lec 15, slide 32.
        Used for AND queries
    '''
    
    result = list()

    # indices to keep track of position in posting
    i1 = 0 
    i2 = 0 
    
    while (i1 < len(p1) and i2 < len(p2)):
        posting1 = p1[i1]
        posting2 = p2[i2]

        # if the docIDs match, append to the result
        if posting1[0] == posting2[0]:
            result.append(posting1)
            i1 += 1
            i2 += 1
        elif posting1[0] < posting2[0]:
            i1 += 1
        else:
            i2 += 1

    return result
    

def process_query(query : [str]) -> [(int, int)]:
    ''' Assuming there are atleast two tokens to process 
        Returns list of resulting postings, sorted by frequency 
        in descending order
    '''
    global QUERY_POSTINGS
    result = list()
    start = perf_counter()
    # sort list of dict keys by len of the postings in descending order
    QUERY_POSTINGS = sorted(QUERY_POSTINGS, key=lambda key: len(QUERY_POSTINGS[key]))

    # get the intersections for each token
    for token in QUERY_POSTINGS:
        if len(result) == 0:
            # result.extend(get_postings)
            result.extend(get_postings(token))
        else:
            result.extend(intersect(result, get_postings(token)))

    # sort result by tf idf in descending order
    result = sorted(result, key = lambda posting: posting[1]+posting[2], reverse = True)
    end = perf_counter()
    print("Search time elapsed: {} ms".format( (end-start) * 1000))
    return result

    
def get_url_names(postings : [[int]]) -> [str]:
    ''' Given the results {docID:scores} dict, return a list of corresponding URLs '''
    global url
    result = list()
   
    for posting in postings:
        doc_id = 0
        result.append(parse.defrag_url(url[posting[doc_id]]))
    return result

def is_valid(url : str) -> str:
    # invalid_file_types = [".ph", ".tx", ".htm", "prog", ".ht"]
    for filetype in invalid_file_types:
        if url.endswith(filetype):
            return False
    return True

def get_query_terms(query_str : str, stopwords: [str]) -> [str]:
    '''Returns a list of stemmed tokens...
    '''
    
    ps = PorterStemmer()
    result = list()
    '''
    for token in re.split("\W+\|\|\W+", query_str):
        if token not in stopwords:
            result.append(ps.stem(token))
    
    for token in re.findall("!\W+", query_str):
        if token[1:] not in stopwords:
            result.append(ps.stem(token))
    '''

    for token in re.findall("\w+", query_str):
        stemmed_tok = ps.stem(token)
        if (token not in stopwords) and (stemmed_tok not in result):
            result.append(stemmed_tok)

    return result

def get_query_postings(query_list : [str]) -> dict:
    ''' Returns dict mapping stemmed token to posting 
    '''
    postings = dict()
    for token in query_list:
        if token not in postings:
            postings[token] = get_postings(token)
    return postings

def load_stopwords():
    result = list()
    with open("stopwords.txt", "r") as f:
        for line in f:
            result += line.strip()
    return result

def get_k_results(result_urls:[str], k:int) -> [str]:
    if k > len(result_urls):
        k = len(result_urls)
    elif k < 0:
        k = 0

    k_results = OrderedDict()

    for i in result_urls:
        if len(k_results) == k:
            break
        if i not in k_results:
            k_results[i] = 0
        
    
    return k_results.keys()
        
    
if __name__ == "__main__":

    # DOC_COUNT = 55_393

    ''' Load in the goods '''
    print("Loading search engine...")

    url = parse.load_bin("url.bin")
    doc = parse.load_bin("doc.bin")
    stopwords = load_stopwords()

    index_index = parse.load_bin("index_index.bin")

    with open("merged_index.txt", "r") as merged_index:
        print("Done.")
        ''' Getting query input '''

       
        while True:
            query = input("Input query: ")
            if query == ":q":
                break
            
            
            QUERY_TERMS = get_query_terms(query, stopwords)

            QUERY_POSTINGS = get_query_postings(QUERY_TERMS)
            result = process_query(QUERY_TERMS)

            # # Printing the results
            result_urls = get_url_names(result)
            result_set = get_k_results(result_urls, int(k))

            print("Results obtained: {}".format(len(result_set)))
            k = input("How many results to show? ")
            for i in result_set:
                print(i)
            
        


    


