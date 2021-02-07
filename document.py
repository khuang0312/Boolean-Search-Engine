from math import log10, log

# This defines a Document class
# A Document represents a processed website

class Document:
    def __self__(self, name):
        self.name = name # the document file the token was found in
        
        # keep track of amount of unique tokens (terms)
        # this avoids using len(self.term_frequencies)
        self.terms = 0
        
        # this maps tokens (terms) to amount of occurences in the doc...
        self.term_frequencies = {}
    
    # Numerous ways of calculating the term frequency is provided down here
    # This gives us a variety of options
    # The easiest to use is the raw frequency (raw_freq)
    def bool_freq(self, term: str) -> int:
        '''Returns 1 if term occurs in document and 0 otherwise
        '''
        return 1 if term in term_frequencies else 0
    
    def raw_freq(self, term : str) -> int:
        '''raw_freq returns the raw count of a term in a document...
        '''
        if term not in term_frequencies:
            return 0
        else:
            return term_frequencies[term]
    
    def adj_freq(self, term : str) -> int:
        '''returns raw_freq divide by number of words in d to adjust
        for document length
        '''
        if term not in term_frequencies:
            return 0
        else:
            return term_frequencies[term] / self.terms

    def log_freq(self, term : str) -> int:
        '''return log(1+raw_frequencies)
        '''
        return log10(1 + self.raw_freq(term))
    
    def aug_freq(self, term : str) -> int:
        '''augmented frequency prevents bias over longer documents
        
        returns the raw_frequency of the word over raw frequency 
        of most occuring term in document
        '''
        freq_ratio = raw_freq(term) / max(self.term_frequencies.values())
        return 0.5 + (0.5 * freq_ratio)
    
    def __eq__(self, other : Document) -> bool:
        '''Two postings are identical if they have the same name
        '''
        return self.name == other.name
