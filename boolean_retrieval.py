import sys
import pickle
import re
from nltk.stem import PorterStemmer
import parse
from timer import Timer, to_milliseconds

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
    

def process_query(query : str) -> [(int, int)]:
    ''' Assuming there are atleast two tokens to process 
        Returns list of resulting postings, sorted by frequency 
        in descending order
    '''
    result = list()
    query_index = dict()
    tokens = re.split("\W+|\W+and\W+", query) # gets the individual terms, return ['a', 'b', 'c', 'd']
    ps = PorterStemmer()

    
    # get the postings
    for i in range(len(tokens)):
        tokens[i] = ps.stem(tokens[i])
        query_index[tokens[i]] = get_posting(tokens[i])
    
    # sort list of dict keys by len of the postings in descending order
    query_index = sorted(query_index, key=lambda key: len(query_index[key]))

    # get the intersections for each token
    for token in query_index:
        if len(result) == 0:
            result.extend(index[token])
        else:
            result.extend(intersect(result, index[token]))

    # sort result by word freq in descending order
        # only good for M2. Was scoring/ranking by raw term frequency
    # result = sorted(result, key = lambda posting: posting[1], reverse = True)

    return result
