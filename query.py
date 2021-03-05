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

def get_postings(token : str) -> [tuple]:
    ''' Returns the postings of the given token 
        CURRENTLY ONLY WORKS FOR IN MEMORY INDEX
    '''
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
    for n in weights:
        val += n ** 2
    doc_length = sqrt(val)
    return doc_length

def get_query_tfidf_vectors(query : [str]) -> dict:
    ''' Calcuates ALL tf-idf vectors for the given query token.
        Includes normalize value
        key = token | value = tf-idf vector
    '''
    # global DOC_COUNT
    result = OrderedDict()
    weights = list()
    word_freq = computeWordFrequency(tokens)

    ''' Calculate the vector (except for normalized value) '''
    for token in query:
        df = len(get_postings(token))
        tf_wt = 1+log10(word_freq[token])
        idf = log10(DOC_COUNT / df)
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
    # for token in doc_vectors:
    #     weights.append(doc_vectors[token]["wt"])
    
    doc_length = get_doc_length(weights)

    for token in doc_vectors:
        doc_vectors[token]["normalize"] = doc_vectors[token]["wt"] / doc_length
    
    return doc_vectors


def process_query(query : str) -> dict:
    ''' Returns a dict of docIDs and their scores
    '''
    start = perf_counter()

    ''' stem the tokens '''
    ps = PorterStemmer()
    tokens = [ps.stem(token) for token in query.split()]

    ''' calculate query vector '''
    query_tfidf_vector = get_query_tfidf_vectors(query) # dict of vectors for each token in query
    
   

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

if __name__ == "__main__":

    DOC_COUNT = 55_393

    ''' Load in the goods '''
    print("Loading index into memory...")

    url = parse.load_bin("testing/url.bin")
    merged_index = parse.load_bin("testing/index.bin") # temp, replace with txt index later
    
    print("Done.")

    ''' Getting query input '''
    
    while (1):
        query = input("Input query: ")
        

        result = process_query(query)

        
        

        ''' Printing the results '''
        result_urls = get_url_names(result)
        top5 = list()
        n=0
        while n < 5:
            url = transform_url(result_urls[i])
            url = url[:url.find("#")]

            if url not in top5:
                top5.append(url)
        
        for url in top5:
            print(url)
        print()


    


