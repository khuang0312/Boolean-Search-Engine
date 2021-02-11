from math import log10
from parse import page_text, get_words

# document.json
'''
{
    'document1_filepath' : {
        "file_name" : str,      // for convenience 
        "term_count" : int,     // the amount of unique terms in the file
        "term_frequencies" : {  // the occurences of each unique term
            "word1" : int,
            "word2" : int,
            ...
        }
    },

    'document2_filepath' : ...
}
'''

def bool_freq(term_frequencies : dict, term: str) -> int:
    '''Returns 1 if term occurs in document and 0 otherwise
    '''
    return 1 if term in term_frequencies else 0

def raw_freq(term_frequencies : dict, term : str) -> int:
    '''raw_freq returns the raw count of a term in a document...
    '''
    if term not in term_frequencies:
        return 0
    else:
        return term_frequencies[term]
    
    
def adj_freq(term_frequencies : dict, term : str) -> int:
    '''returns raw_freq divide by number of words in d to adjust
        for document length
    '''
    if term not in term_frequencies:
        return 0
    else:
        return term_frequencies[term] / len(term_frequencies)

def log_freq(term_frequencies : dict, term : str) -> int:
    '''return log(1+raw_frequencies)
    '''
    return log10(1 + raw_freq(term_frequencies, term))
    
def aug_freq(term_frequencies : dict, term : str) -> int:
    '''augmented frequency prevents bias over longer documents
        
    returns the raw_frequency of the word over raw frequency 
    of most occuring term in document
    '''
    freq_ratio = raw_freq(term) / max(term_frequencies.values())
    return 0.5 + (0.5 * freq_ratio)

