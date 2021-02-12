from math import log10

from os import walk
from document import raw_freq
import parse
import json


# A diagram of index.json
'''
{
    // tokens -> {}

    'token1' : [{doc_id : int, tf_idf : int}]
}
'''

DOCUMENTS_FOLDER = "DEV/"
DOCUMENTS_JSON = "documents"
INDEX_JSON = "index"
REPORT_JSON = "report"
BATCH_SIZE = 300000
MAX_DOCS = 55393

# The inverted index creates a mapping between tokens and postings
class InvertedIndex:
    def __init__(self, folder : str):
        '''Sets up files to serialize into as well as variables for analytics...
        '''
        
        # batch
        self.batch = 0 # this indicates which files to read from... starts at 0
        self.index = dict()
        self.documents = list()

        #parse.write_json(DOCUMENTS_JSON+str(self.batch), [])
        #parse.write_json(INDEX_JSON+str(self.batch), {})
        #parse.write_json(REPORT_JSON, {})
        
        # folder
        self.folder = folder

        # analytics
        self.total_docs = 0 
        self.unique_words = 0
    

    def process_files(self) -> None:
        for domain, dir, pages in walk(self.folder):
            
            for page in pages:
                self.total_docs += 1
                print("Docs Parsed:", self.total_docs, "Words found:", self.unique_words)
                path = domain + "/" + page
                
                

                if (len(self.index) >= BATCH_SIZE or (len(self.index) < BATCH_SIZE and self.total_docs == MAX_DOCS)):
                    print("Batch {}".format(self.batch))
                    parse.write_json(INDEX_JSON+str(self.batch), self.index)
                    parse.write_json(DOCUMENTS_JSON+str(self.batch), self.documents)
                    self.index = dict()
                    self.documents = list()
                    self.batch += 1
                    #parse.write_json(DOCUMENTS_JSON+str(self.batch), []) # make new files
                    #parse.write_json(INDEX_JSON+str(self.batch), {})

                
                self.documents.append(path)
                term_count, term_frequencies = parse.get_words(parse.page_text(path))
                
                for term in term_frequencies:
                    if term not in self.index:
                        self.index[term] = []
                        self.unique_words += 1
                    self.index[term].append({"doc_id" : self.total_docs, "tf_idf" : term_frequencies[term]})
                
                
                
                '''
                terms_in_prev_index = set()
                

                
                for i in range(self.batch+1):
                    prev_index = parse.load_json(INDEX_JSON+str(i))
                    for term in term_frequencies:
                        if term in prev_index:
                            prev_index[term].append({"doc_id" : self.total_docs, "tf_idf" : term_frequencies[term]})
                            terms_in_prev_index.add(term)
                            continue
                    parse.write_json(INDEX_JSON+str(i),  prev_index)

                for term in [k for k in term_frequencies.keys() if k not in terms_in_prev_index]:
                    if term not in self.index:
                        self.index[term] = []
                        self.unique_words += 1
                    self.index[term].append({"doc_id" : self.total_docs, "tf_idf" : term_frequencies[term]})
                '''

                '''
                for term in term_frequencies:
                    # check to see if token exists in previous index files
                    for i in range(self.batch+1): # self.batch + 1 reflects actual amount of batches
                        prev_index = parse.load_json(INDEX_JSON+str(i));
                        if term in prev_index:
                            
                            prev_index[term].append({"doc_id" : self.total_docs, "tf_idf" : term_frequencies[term]})
                            parse.write_json(INDEX_JSON+str(i),  prev_index)
                            break;
                    else: # if it doesn't...
                        if term not in self.index:
                            self.index[term] = []
                            self.unique_words += 1
                        self.index[term].append({"doc_id" : self.total_docs, "tf_idf" : term_frequencies[term]})
                '''
                
                
                
                
                
                
                
                
                '''
                New attempt
                print(self.total_docs)
                
                
                
                '''

                '''
                # process document
                # create document object
                # serialize into documents dict
                documents_dict = parse.load_json(DOCUMENTS_JSON)
                # reference document.py to understand what's going on here
                documents_dict[id_num] = {"file_name" : page, "term_count" : term_count, "term_frequencies" : term_frequencies}
                parse.write_json(DOCUMENTS_JSON, documents_dict)
                
                # take tokens from document
                # serialize token into tokens dict
                if self.unique_words % 10000 == 0:
                    pass    

                tokens_dict = parse.load_json(INDEX_JSON)
                for term in term_frequencies:
                    if term not in tokens_dict:
                        self.unique_words += 1
                        tokens_dict[term] = {}
                    tokens_dict[term][path] = {"raw_freq" : raw_freq(term_frequencies, term)} 
                parse.write_json(INDEX_JSON, tokens_dict)
                '''
                
    def calculate_tf_idf(self): 
        tokens_dict = parse.load_json(INDEX_JSON)

        for token in tokens_dict:
            for path in tokens_dict[token]:
                # calculate idf
                idf = self.normal_idf(token)
                tdf = tokens_dict[token][path]["raw_freq"]

                tokens_dict[token][path]["tf-idf"] = tdf * idf

        parse.write_json(INDEX_JSON, tokens_dict)


    '''
    {
        // tokens -> {}

        'token1' : [{doc_id : int, tf_idf : int}]
    }
    '''
    def create_analytics(self):
        def getTokenGroup(token):
            if (ord(token[0]) >= ord('a') and ord(token[0]) <= ord('o')):
                #a-o
                return "a_to_o"
            elif (ord(token[0]) >= ord('p') and ord(token[0]) <= ord('z')):
                #p-z
                return "p_to_z"
            else:
                #starts with a number
                return "numbers"
        print("Report")
        GROUPS = ["numbers", "a_to_o", "p_to_z"]
        report_batch = [0, 0, 0]
        MAX_GROUP_SIZE = 150000
        
        #inGROUP1 = lambda x: ord(x[0]) >= ord('a') and ord(x[0]) <= ord('o')
        #inGROUP2 = lambda x: ord(x[0]) >= ord('p') and ord(x[0]) <= ord('z')
        
        self.unique_words = 0
        
        token_groups = {GROUPS[0] : dict(), GROUPS[1] : dict(), GROUPS[2]: dict()}
        batch_index = 0
        tokens_batch = dict()
        while True:
            try:
                tokens_batch = parse.load_json(INDEX_JSON+str(batch_index))
            except OSError as e:
                print(e.errno)
                break
            for token in tokens_batch:
                token_group = getTokenGroup(token)
                if token not in token_groups[token_group]:
                    token_groups[token_group][token] = list()
                    self.unique_words += 1
                for obj in tokens_batch[token]:
                    token_groups[token_group][token].append(obj)
            batch_index += 1

        for token_group in GROUPS:
            print("writing", str(token_group), "to", str(token_group) + ".json")
            parse.write_json(token_group, token_groups[token_group]) 
        parse.write_json(REPORT_JSON, {"total_docs": self.total_docs, "unique_words": self.unique_words})
        print("total_docs", self.total_docs, "unique_words", self.unique_words)


        '''
        for i in range(6): #self.batch
            print("Batch", i)
            tokens_batch = parse.load_json(INDEX_JSON+str(i))
            
            for token in tokens_batch:
                token_group = GROUPS[0]
                
                if inGROUP1(token):
                    token_group = GROUPS[1]
                elif inGROUP2(token):
                    token_group = GROUPS[2]
                
                dct = token_groups[token_group]

                if token not in dct:
                    dct[token] = []
                    # self.unique_words += 1
                    unique_words += 1
                    print(unique_words)
                dct[token] += tokens_batch[token]
                
                if len(dct) > MAX_GROUP_SIZE or i == 5:
                    group_num = GROUPS.index(token_group)
                    
                    if (report_batch[group_num] - 1 >= 0):
                        print("loading previous {} {}".format(token_group, report_batch[group_num] - 1))
                        prev_dct = parse.load_json(token_group+str(report_batch[group_num] - 1))
                        for k in prev_dct:
                            if k not in dct:
                                dct[k] = []
                            dct[k] += prev_dct[k]
                    
                    print("writing {} {}".format(token_group, report_batch[group_num]))
                    parse.write_json(token_group+str(report_batch[group_num]), dct)
                    token_groups[token_group] = {}
                    print({k : len(token_groups[k]) for k in token_groups})
                    report_batch[group_num] += 1
            
        for i in range(len(GROUPS)):
            print(len(parse.load_json(GROUPS[0])) )
            print(len(parse.load_json(GROUPS[1])) )
            print(len(parse.load_json(GROUPS[2])) )
        print("Unique words:", unique_words)
        '''
        
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
<<<<<<< HEAD
    inverted_index.process_files()
=======
    #inverted_index.process_files()
>>>>>>> c28d0a9bb7df579c3d2725bd5fea42d0906fe7f7
    inverted_index.create_analytics()
