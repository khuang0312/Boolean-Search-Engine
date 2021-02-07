from math import log10, log


# The inverted index creates a mapping between tokens and postings
class InvertedIndex:
    def __self__(self):
        # parse the files...
        # create postings...
        pass

    def unary_idf(self, term):
        return 1

    def normal_idf(self, term):
        '''total number of documents by 
        number of documents containing term
        '''
        
        return log10()
        
if __name__ == "__main__":
    # create an array of documents... and an counter of documents
        # as we create the documents, add their terms to a map of terms to frequencies...
            # for i in documetns.terms_frequencies:
                # global_frequencies[i] += 1...

    # create an mapping of tokens to postings
        # for d in documents:
        #  tp{token}.append(Posting(d.name, tf_idf score))
            

    # calculate the idf by getting the total number of documents containing each term
