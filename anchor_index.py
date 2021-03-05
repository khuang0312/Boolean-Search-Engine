from os import walk
from os.path import getsize
import json
import pickle
from bs4 import BeautifulSoup
import parse
import requests

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

if __name__ == "__main__":
    
    url = "https://aiclub.ics.uci.edu/"
    
    soup = 
    # anchor_index = dict() # docID : position
    # index = SortedDict() # docID : anchor text

    # docs  = []
    # urls = []

    # doc_id = 1
    # for domain, dir, pages in walk("DEV/"):
    #     for page in pages:
    #         print("Parsing doc {}".format(doc_id)
            
    #         doc_path = domain + "/" + page
    #         page_data = page_text(doc_path)
            
    #         tokens = get_words(page_data[0])
            
    #         doc_id += 1
    # print("Done.")