import sys
import pickle
import re
from nltk.stem import PorterStemmer
import parse
from math import log10, sqrt
from time import perf_counter
from collections import OrderedDict

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

def get_postings(token : str) -> [list]:
    ''' Returns the postings of the given token 
    '''
    try:
        global merged_index
        seek = int(index_index[token])
        merged_index.seek(seek)
        # werner [[30886, 6.258362786994808, 375, 4964, 5000], [30936, 4.236864622317388, 526]]
        line = merged_index.readline()
        print(line)
        return eval(line.split()[1])
    except KeyError:
        print("Token \'{}\' not found!".format(token))

def get_doc_length(weights:[int]) -> float:
    ''' Given the list of wt values (query or doc), calculate the normalized value '''
    val = 0
    for n in weights:
        val += n ** 2
    doc_length = sqrt(val)
    return doc_length

def get_query_tfidf_vectors(query : [str]) -> dict:
    ''' Calcuates ALL tf-idf vectors for the given query token.
        Includes normalize value
        key = token | value = tf-idf vector
    '''
    global QUERY_POSTINGS
    result = OrderedDict()
    weights = list()
    word_freq = computeWordFrequency(query)

    ''' Calculate the vector (except for normalized value) '''
    for token in query:
        if token not in result:
            df = len(QUERY_POSTINGS[token])
            tf_wt = 1+log10(word_freq[token])
            idf = log10(55_393 / df)
            wt = tf_wt * idf
            tfidf_vector = {
                "wt" : wt,
                "normalize" : 0,
            }
            weights.append(wt)
            result[token] = tfidf_vector

    ''' Calculate normalized value '''
    doc_length = get_doc_length(weights)
    for token in result:
        result[token]["normalize"] = result[token]["wt"] / doc_length

    return result

def get_doc_posting(token : str, docID : int) -> list:
    ''' Get the posting for the given token and docID
    '''
    global QUERY_POSTINGS
    for posting in QUERY_POSTINGS[token]:
        if posting[0] == docID:
            return posting
    return []

def get_document_tfidf_vector(token : str, docID : int) -> dict:
    ''' Calculates the weighted tf-idf vector for the given token.
        Still need to calculate "normalize" value
        Token should already be stemmed
    '''
    posting = get_doc_posting(token, docID)
    tf_raw = len(posting) - 2
    tf_wt = 1+log10(tf_raw)

    result = {
        "wt" : tf_wt, 
        "normalize" : 0,
        } 
    
    return result

def get_doc_vectors(query_tokens : [str]) -> dict:
    ''' Given the list of stemmed query tokens,
        Calculate doc vectors for cosin similarity scoring
    '''
    doc_vectors = dict()
    for token in query_tokens:
        postings_list = get_postings(token)
        for doc in postings_list:
            docID = doc[0]
            vector = get_document_tfidf_vector(token, docID)
            if docID not in doc_vectors:
                doc_vectors[docID] = {token : vector}
            else:
                doc_vectors[docID][token] = vector 
    return doc_vectors

def normalize_doc_wts(doc_vectors : dict): 
    ''' 
    {
        token : vector dict,
        token : vector dict
    }
    '''
    weights = list()
    weights = [doc_vectors[token]["wt"] for token in doc_vectors]
    
    doc_length = get_doc_length(weights)

    for token in doc_vectors:
        doc_vectors[token]["normalize"] = doc_vectors[token]["wt"] / doc_length
    
    return doc_vectors


def process_query(query : [str]) -> dict:
    ''' Returns a dict of docIDs and their scores. Query tokens should already be stemmed
    '''
    start = perf_counter()

    ''' calculate query vector '''
    # dict of vectors for each unique token in query
    query_tfidf_vector = get_query_tfidf_vectors(query) 
    
    ''' calculate doc vectors '''
    # docID : {
    #     "token1" : {vector dict},
    #     "token2" : {vector dict}, ...
    # }
    
    doc_vectors = get_doc_vectors(tokens) 
    
    ''' Normalize doc vector weights '''
    for docID in doc_vectors:
        doc_vectors[docID] = normalize_doc_wts(doc_vectors[docID])

    ''' Calculate scores ''' 
    scores = dict()
    for docID in doc_vectors:
        result = 0
        for token in query_tfidf_vector:
            if token in doc_vector[docID]:                
                result += doc_vector[docID][token]["normalize"] * query_tfidf_vector[token]["normalize"]
    scores = sorted(scores.items(), key=lambda x:x[1])
   
    print("Search time elapsed: {} ms".format( (perf_counter()) - start * 1000))
    return scores
    
# def get_url_names(postings : [(int, int)]):
#     ''' Given the list of postings, return a list of the 
#         associated URLs
#     '''
#     global url
#     result = list()
#     # print("posting: {}".format(postings))
#     for posting in postings:
#         ID = posting[0]
#         print(ID)
#         result.append(url[ID])

#     return result

def get_url_names(scores : dict) -> [str]:
    ''' Given the results {docID:scores} dict, return a list of corresponding URLs '''
    global url
    result = list()
    for docID in scores:
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

def get_query_terms(query_str : str) -> [str]:
    '''Returns a list of stemmed tokens...
    '''
    ps = PorterStemmer()
    return [ps.stem(token) for token in query_str.split()]

def get_query_postings(query_list : [str]) -> dict:
    ''' Returns dict mapping stemmed token to posting 
        
    '''
    postings = dict()
    for token in query_list:
        if token not in result:
            postings[token] = get_postings(token)
    return postings


    
    
if __name__ == "__main__":

    # DOC_COUNT = 55_393

    ''' Load in the goods '''
    print("Loading search engine...")

    url = parse.load_bin("url.bin")
    doc = parse.load_bin("doc.bin")
    index_index = parse.load_bin("index_index.bin")

    with open("merged_index.txt", "r") as merged_index:
        print("Done.")
        ''' Getting query input '''
        while True:
            query = input("Input query: ")
            if query == ":q":
                break
            
            QUERY_TERMS = get_query_terms(query)
            QUERY_POSTINGS = get_query_postings(query_list)

            result = process_query(QUERY_TERMS)

            ''' Printing the results '''
            result_urls = get_url_names(result)


    


