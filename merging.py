import pickle
from itertools import zip_longest
from pickled_index import load_bin

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

if __name__ == "__main__":
    index_index = load_bin("index_index.bin")
    game1 = [(11, 3), (17, 2), (26, 1), (33, 2), (35, 4), (53, 1), (83, 2), (88, 1)]
    game2 = [(110, 1), (119, 2), (128, 1), (147, 2), (164, 4), (167, 4), (171, 4)]
    
    index1 = open("index1.txt", "r")
    index2 = open("index2.txt", "r")
     
    for i in zip_longest(index1, index2, fillvalue=tuple()):
        
    print(result)
    
