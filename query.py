import sys
import pickle
import re
from nltk.stem import PorterStemmer
import parse
from timer import Timer, to_milliseconds
import math
import time

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

def computeWordFrequency(tokens:[str]) -> dict:
    result = dict()
    for token in tokens:
        result[token] = result.get(token,0) + 1
    return result

def get_postings(token : str) -> [tuple]:
    ''' Returns the postings of the given token '''
    try:
        global merged_index
        return  merged_index[token]
    except KeyError:
        print("Token \'{}\' not found!".format(token))

def get_doc_posting(token : str, docID : int) -> list:
    ''' Get the posting for the given token and docID
    '''
    for posting in get_postings(token):
        if posting[0] == docID:
            return posting
    return []

def get_doc_length(weights:[int]) -> float:
    ''' Given the list of wt values (query or doc), calculate the normalized value '''
    val = 0
    for n in weight:
        val += n ** 2
    doc_length = math.sqrt(val)
    return doc_length


def get_query_tfidf_vector(query : str) -> dict:
    ''' Calcuates ALL tf-idf vectors for the given query.
        Includes normalize value
        key = token | value = tf-idf vector
    '''
    global DOC_COUNT
    ps = PorterStemmer()
    tokens = [ps.stem(token) for token in query.split()]
    result = dict()
    weights = list
    word_freq = computeWordFrequency(tokens)

    ''' Calculate all the vectors (except for normalized value) '''
    for token in tokens:
        df = len(get_postings[token])
        tf_wt = 1+log10(word_freq[token])
        idf = log10(DOC_COUNT / df)
        wt = tf_wt * idf
        tfidf_vector = {
            "tf-raw" : word_freq[token],
            "tf-wt" : tf_wt,
            "df" : df,
            "idf" : idf,
            "wt" : wt,
            "normalize" : 0
        }
        weights.append(wt)
        result[token] = tfidf_vector

    ''' Calculate normalized calue '''
    doc_length = get_doc_length(weights)
    for token in result:
        result[token]["normalize"] = result[token]["wt"] / doc_length

    return result

def get_document_tfidf_vector(token : str, docID : int) -> dict:
    ''' Calculates the weighted tf-idf vector for the given token.
        Still need to calculate normalize value.
    '''
    ps = PorterStemmer()
    token = ps.stem(token)
    posting = get_doc_posting(token, docID)
    tf_raw = len(posting) - 2
    tf_wt = 1+log10(tf_raw)

    result = {
        "tf-raw": tf_raw, 
        "tf-wt" :  tf_wt,
        "wt" : tf_wt, 
        "normalize" : 0} 
    
    return result

def process_query(query : str) -> [str]:
    ''' Returns a list of resulting URLs using the given query
        
    '''
    query_tfidf_vector = get_query_tfidf_vector(query)
    


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

    DOC_COUNT = 55_393

    ''' Load in the goods '''
    # print("Loading index into memory...")

    # url = parse.load_bin("url.bin")
    # merged_index = parse.load_bin("index.bin") # temp, replace with txt index later
    
    # print("Done.")

    ''' Getting query input '''
    
    while (1):
        query = input("Input query: ")
        start = time.time()

        # result = process_query(query)

        end = time.time()
        print("Search time elapsed: {} s".format(end - start))

        # result_urls = get_url_names(result)

        # r = 0
        # i = 0
        # top5 = list()

        # while r < 5:
        #     url = transform_url(result_urls[i])
        #     url = url[:url.find("#")]

        #     if url not in top5:
        #         top5.append(url)
        #         r += 1
        #     i += 1
        
        # for url in top5:
        #     print(url)
        # print()


    


