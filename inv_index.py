from math import log10

from os import walk
from document import raw_freq
import parse
import json


# A diagram of index.json
'''
{
    // tokens -> "posting dicts"
    // postings are the filepath to a dict of attributes important to postings
    // tdf-idf scores for instance...
    // "postings" might have important attributes 
    // keeping postings in a dict improves access speed of specific postings

    'token1' : {'path1' : {'tdf-idf' : int}, 'path2' : {...}},
}
'''


DOCUMENTS_FOLDER = "DEV/"
DOCUMENTS_JSON = "documents"
INDEX_JSON = "index"
REPORT_JSON = "report"


# The inverted index creates a mapping between tokens and postings
class InvertedIndex:
    def __init__(self, folder : str):
        '''Sets up files to serialize into as well as variables for analytics...
        '''
        parse.write_json(DOCUMENTS_JSON, {})
        parse.write_json(INDEX_JSON, {})
        parse.write_json(REPORT_JSON, {})
        
        # folder
        self.folder = folder

        # analytics
        self.total_docs = 0 
        self.unique_words = 0
    

    def process_files(self) -> None:
        for domain, dir, pages in walk(self.folder):
            for page in pages:
                self.total_docs += 1
                path = domain + "/" + page
                print(self.total_docs, path) # DEBUG
                term_count, term_frequencies = parse.get_words(parse.page_text(path))
                
                # process document
                # create document object
                # serialize into documents dict
                documents_dict = parse.load_json(DOCUMENTS_JSON)
                # reference document.py to understand what's going on here
                documents_dict[path] = {"file_name" : page, "term_count" : term_count, "term_frequencies" : term_frequencies}
                parse.write_json(DOCUMENTS_JSON, documents_dict)
                
                # take tokens from document
                # serialize token into tokens dict
                if self.unique_words % 10000 == 0:
                    

                tokens_dict = parse.load_json(INDEX_JSON)
                for term in term_frequencies:
                    if term not in tokens_dict:
                        self.unique_words += 1
                        tokens_dict[term] = {}
                    tokens_dict[term][path] = {"raw_freq" : raw_freq(term_frequencies, term)} 
                parse.write_json(INDEX_JSON, tokens_dict)
        
    def calculate_tf_idf(self): 
        tokens_dict = parse.load_json(INDEX_JSON)

        for token in tokens_dict:
            for path in tokens_dict[token]:
                # calculate idf
                idf = self.normal_idf(token)
                tdf = tokens_dict[token][path]["raw_freq"]

                tokens_dict[token][path]["tf-idf"] = tdf * idf

        parse.write_json(INDEX_JSON, tokens_dict)
                          
    def unary_idf(self, term):
        return 1

    def normal_idf(self, term):
        '''log of total number of documents by 
        number of documents containing term plus 1 

        We add 1 in the denominator to avoid division by 0...
        '''
        docs_with_term = 0
        documents_dict = parse.load_json(DOCUMENTS_JSON)
        for path in documents_dict:
            if term in documents_dict[path]["term_frequencies"]:
                docs_with_term += 1

        return log10(self.total_docs / (docs_with_term + 1))
        
if __name__ == "__main__":
    inverted_index = InvertedIndex(DOCUMENTS_FOLDER)
    inverted_index.process_files()
    inverted_index.calculate_tf_idf()
