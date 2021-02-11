from math import log10

from os import walk
from document import Document

def _create_doc_arr(folder):
    '''returns list of Document objects, count of Documents, and
        a set of global tokens
        
       this is a private helper method used to construct an
       InvertedIndex
    '''
    documents = []
    documents_len = 0
    
    # goes through files...
    for domain, dir, pages in walk(folder):
        for p in pages:
            path = domain + "/" + p
            doc = Document(path)
            print(doc.term_frequencies)
            documents.append(doc)

# The inverted index creates a mapping between tokens and postings
class InvertedIndex:
    def __init__(self, folder : str):
        _create_doc_arr(folder);



                          
    def unary_idf(self, term):
        return 1

    def normal_idf(self, term):
        '''total number of documents by 
        number of documents containing term
        '''
        
        return log10()
        
if __name__ == "__main__":
    # Create an array of documents and an counter of documents
    # We need the amount of documents to calculate idf later.
    # It also avoids us having to use len on the array of documents.

    # As you create a document, add the terms to a dictionary mapping 
    # terms among all the documents to the amount of documents containing that term
    
    # for example
    # for i in documents.terms_frequencies:
        # global_frequencies[i] += 1
    
    # calculate the idf by getting the total number of documents containing each term
    
    # Create a dictionary mapping tokens to postings by iterating through
    # the array of documents...

    # for example
    # for d in documents:
    #   #calculate tf_idf_score at this point...
    #   token_to_posting[token].append(Posting(d.name, tf_idf_score))
    
    # save it to a file probably


    # this contains the main routine for the program
    InvertedIndex("DEV/")
