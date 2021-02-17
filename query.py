import sys
import pickle

'''
Queries to test:

cristina lopes
machine learning
ACM
master of software engineering
'''

'''
INDEX DATA STRUCTURE
{token : [(doc_id, raw frequency)]}

HOW 2 QUERY
- get the posting for each token in query -> store in dict
- sort postings by doc ID 
    (should already be sorted since docIDs are assigned sequentially when the index is created)
- sort dict by length of postings in descending order
- intersect() for merging two postings
    returns list of docIDs
- process_query() for merging all postings (while loop)
    returns list of docIDs
'''


''' 
REGEX PATTERNS

re.split("\W+", "a b      c     ; d") # gets the individual terms, return ['a', 'b', 'c', 'd']

'''
def load_file(file_name : str):
    '''Wrapper for loading a file
    '''
    obj = None
    with open(file_name, "rb") as f:
        obj = pickle.load(f, encoding="UTF-8")
    return obj

def get_postings(token : str) -> [tuple]:
    ''' Returns the postings of the given token '''
    return index[token]


def intersect(p1 : list, p2 : list) -> [(int, int)]:
    ''' Given two sorted (by docID) postings lists, merge them 
        together into a single list. 
        Returns list of tuples (docIDs, term freq).
        len(p1) must be less than len(p2).
        Used psudeo code form lec 15, slide 32.
    '''
    result = list()

    # indices to keep track of position in posting
    i1 = 0 
    i2 = 0 
    
    while (i1 < len(p1) and i2 < len(p2)):
        posting1 = p1[i1]
        posting2 = p1[i2]
        
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
    ''' Assuming there are atleast two tokens to process '''
    result = list()
    query_index = dict()
    tokens = re.split("\W+|\W+and\W+", query) # gets the individual terms, return ['a', 'b', 'c', 'd']

    # get the postings
    for token in tokens:
        query_index[token] = get_postings(token)
    
    # sort dict by len of postings in descending order
    query_index = sorted(query_index, key=lambda key: len(query_index[key]))

    # get the intersections for each token
    for token in query_index:
        
        if len(result) == 0:
            result.extend(index[token])
        else:
            result.extend(intersect(result, query_index[token]))

    return result


if __name__ == "__main__":
    args = sys.argv
    query = args[1:]

    index = load_file("index.bin")
    doc = load_file("doc.bin")
