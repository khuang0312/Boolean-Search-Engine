from os import walk
from os.path import getsize
import json
import pickle
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
import re
from sys import argv, getsizeof
from sortedcontainers import SortedDict
import parse




'''
Dictionary of tokens mapped to list of lists [doc_id, tf-idf score, important text score, positions in doc]
'''
def page_text(filepath: str) -> (str, str):
    ''' Returns the page text and URL from the given JSON filename,
        in the following format (page_text, URL)
    '''
    page_text = ""
    url = ""
    with open(filepath) as f:
        html_doc = json.load(f)
        soup = BeautifulSoup(html_doc['content'], "html.parser")
        page_text = soup.get_text()
        url = html_doc["url"]
    return (page_text, url)

def get_words_in_tag_type(filepath: str, tag_name: str) -> [str]:
    '''return tokens inside all occurences of a specific tag
    '''
    tokens = []
    with open(filepath) as f:
        html_doc = json.load(f)
        soup = BeautifulSoup(html_doc['content'], "html.parser")
        tags = soup.find_all(tag_name) # Tag objects...

        for tag in tags:
            # must cast tag to String to soup it
            tag_soup = BeautifulSoup(str(tag), 'html.parser')
            tag_souped = eval("tag_soup." + tag_name, globals(), locals())
            tokens += get_words(str(tag_souped.string)).keys() # tag.string returns NavigableString

    return tokens

def get_words(text : str) -> {str : [int]}:
    '''Uses very simplified rules to get words from the file
        Only lowercase alphanumeric characters

        According to general specifications, we use
        all alphanumeric sequences

        We consider stop words...
    '''
    word_frequencies = {}
    ps = PorterStemmer()

    word_pos = 0
    for word in re.finditer(r'([a-zA-Z0-9]+)', text):
        try:
            word = ps.stem(word.group(0).lower())
        except IndexError:
            print("Something happened with term {}".format(word))
        else:
            if word not in word_frequencies:
                word_frequencies[word] = []
            word_frequencies[word].append(word_pos)
            word_pos += 1
 
    return word_frequencies


def write_index(index : 'SortedDict', index_filename : str):
    ''' writes index to text file '''
    
    with open(index_filename, "w") as f:
        for key in index:
            line = "{} {}\n".format(key, index[key])
            f.write(line)

def index_info(unique_tokens:int=0, doc_count:int=0, partial_indexes:int=0):
    index_info_dict = {}
    index_info_dict["unique_tokens"] = unique_tokens
    index_info_dict["doc_count"] = doc_count
    index_info_dict["partial_indexes"] = partial_indexes
    return index_info_dict
    

if __name__ == "__main__":

    parse.cleanup_files()
    
    BATCH_SIZE = 10_486_240 # in bytes 
    batch_number = 1
    doc_id = 0
    unique_tokens = 0 # probably can't be used anymore

    index_index = dict() # key = token, value = file seeking position
    index = SortedDict() # dict - SortedDict()
    docs  = []
    urls = []

    for domain, dir, pages in walk("DEV/"):
        for page in pages:
            # if batch_number == 3: # needed to stop loop prematurely to test 
            #    print("Did enough testing")
            #    break
            print("Parsing doc {}, Unique Tokens: {}, Size of Index {}".format(
                doc_id, unique_tokens, getsizeof(index)))
            
            doc_path = domain + "/" + page
            page_data = page_text(doc_path)

            docs.append(page)
            urls.append(page_data[1])

            # precompute list of "special tokens"
            h1_tokens = get_words_in_tag_type(doc_path, "h1") # 1
            h2_tokens = get_words_in_tag_type(doc_path, "h2") # .8
            h3_tokens = get_words_in_tag_type(doc_path, "h3") # .6
            strong_tokens = get_words_in_tag_type(doc_path, "strong") # .4
            bold_tokens = get_words_in_tag_type(doc_path, "b") # .3
            
            tokens = get_words(page_data[0])
            for t in tokens:
                if t not in index:
                    index[t] = []
                    unique_tokens += 1 # might have to remove eventually
                score = 0
                if t in h1_tokens:
                    score += 1
                if t in h2_tokens:
                    score += .8
                if t in h3_tokens:
                    score += .6
                if t in strong_tokens:
                    score += .4
                if t in bold_tokens:
                    score += .3
                index[t].append([doc_id, 0, score] + tokens[t]) # the score will be where the tf-idf score goes... 
            doc_id += 1
            
            if getsizeof(index) > BATCH_SIZE:
                # write to file
                index_filename = "index" + str(batch_number) + ".txt"
                print("Writing {} to disk...".format(index_filename))
                write_index(index, index_filename)
                # start empty current index, start a new one
                batch_number += 1
                index = SortedDict()
        
        

        # if batch_number == 3: # needed to stop loop prematurely to test 
        #    break

    if getsizeof(index) > 0: # writes remaining file index
        index_filename = "index" + str(batch_number) + ".txt"
        print("Writing last index to disk")
        print("Writing {} to disk...".format(index_filename))
        write_index(index, index_filename)
        batch_number += 1

    parse.write_bin("doc.bin", docs)         # maps docID to file names
    parse.write_bin("url.bin", urls)         # maps docID to URLs
    index_info_dict = index_info(unique_tokens, doc_id + 1, batch_number) # allows us to calculate tf-idf score later...
    parse.write_bin("index_info.bin", index_info_dict)    
    print("Done.")
    
