import sys
import pickle
import re
from nltk.stem import PorterStemmer

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


def get_posting(token : str) -> [tuple]:
    ''' Returns the postings of the given token '''
    return index[token]

def get_url_names(postings : [(int, int)]):
    ''' Given the list of postings, return a list of the 
        associated URLs
    '''
    result = list()
    for posting in postings:
        ID = posting[0]
        result.append(url[ID])

    return result



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
    
    # sort list of dict keys by len of postings in descending order
    query_index = sorted(query_index, key=lambda key: len(query_index[key]))

    # get the intersections for each token
    for token in query_index:
        if len(result) == 0:
            result.extend(index[token])
        else:
            result.extend(intersect(result, index[token]))

    # sort result by word freq in descending order
    result = sorted(result, key = lambda posting: posting[1], reverse = True)

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
    invalid_file_types = [".ph", ".tx", ".htm", "prog", ".ht"]
    for filetype in invalid_file_types:
        if url.endswith(filetype):
            return False
    return True

if __name__ == "__main__":
    args = sys.argv
    query = " ".join(args[1:])

    # ''' Load in the goods '''
    # print("Loading in index and url...")
    index = load_file("index.bin")
    url = load_file("url.bin")
    # print("Finished loading index and url...")

    ''' Running query '''

    print("Query: '{}'\n".format(query))
    result = process_query(query)
    result_urls = get_url_names(result)

    print("= Top 5 Results =\n")
    r = 0
    i = 0
    top5 = list()

    while r < 5:
        url = transform_url(result_urls[i])
        url = url[:url.find("#")]

        if (url not in top5) and (is_valid(url)):
            top5.append(url)
            r += 1
        i += 1
    
    for url in top5:
        print(url)
    print()

'''
- some urls lead to 404 pages
- some urls dont have the associated token
'''


    


