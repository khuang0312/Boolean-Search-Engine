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
    - Flask - needed for the Web GUI
    - This can be done with the command: ```pip install --user nltk bs4 sortedcontainers flask```
    - Make sure you have the "developer.zip" folder as well.

2. Extract the developer.zip folder so that the resulting "DEV" folder
is in the root directory with the Python code files: 
partial\_index.py, merging.py, and query.py 

3. Run partial\_index.py with the command. ```python3 ./partial_index.py```
This file creates the partial index files. Each partial index file is 
labeled "index\{number\}.txt". Make sure to keep this file running until completion.

4. Run merging.py. ```python3 ./merging.py``` 
This file will merge the partial index files into one complete 
merged index. Make sure to keep this file running until completion.

5. There are two ways of running the program. The first method is 
an command line application. The second one is a website developed using Flask.
   1. Run query.py. ```python3 ./query.py``` You'll be prompted for input. Type in your search terms
and await the results! Type ":q" once you're done to end the program.
   2. Make sure that you can see the desktop. The website can't run in an headless environment.
      - Type the following commands in the terminal. This allows Flask to know where to run the program.
      ```
      export FLASK_APP=searchpage.py
      flask run
      ```
      - In your browser, go to "http://127.0.0.1:5000/". You'll see the site!

