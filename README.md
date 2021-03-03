# CS 121 - Search Engine (M3)
Given search terms, this search engine retrieve documents containing the terms from a folder of documents.

For example, typing the word "acm" will give pages containing the word "acm".

## Team Members
  - Kevin Huang
  - Camille Padua
  - Klim Rayskiy
  - Cedric Lim

## How to Set Up
1. Install the required dependencies and files
    - NLTK 3.5 - needed for PorterStemmer
    - BeautifulSoup 4.9.x - needed for BeautifulSoup
    - sortedcontainers - needed for SortedDict
    - This can be done with the command: ```pip install --user nltk bs4 sortedcontainers```
    - Make sure you have the "developer.zip" folder as well.

2. Extract the developer.zip folder so that the resulting "DEV" folder
is in the root directory with the Python code files: 
partial\_index.py, merging.py, and query.py 

3. Run partial\_index.py. This file creates the partial index files.
Each partial index file is labeled "index\{number\}.txt".

4. Run merging.py. This file will merge the partial index files into 
one complete merged index.

5. Run query.py. You'll be prompted for input. Type in your search terms
and await the results!
