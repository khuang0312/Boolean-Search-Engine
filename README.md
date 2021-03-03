<h1>CS 121 - Search Engine (M3)</h1>
<h2>Team Members</h2>
- Kevin Huang
- Camille Padua
- Klim Rayskiy
- Cedric Lim

<h2>How to Set Up</h2>
1. Install the required dependencies
- NLTK 3.5 - needed for PorterStemmer
- BeautifulSoup 4.9.x - needed for BeautifulSoup
- sortedcontainers - needed for SortedDict

```
pip install --user nltk bs4 sortedcontainers
```

2. Extract the developer.zip folder so that the resulting "DEV" folder
is in the root directory with the Python code files: 
partial\_index.py, merging.py, and query.py 

3. Run partial\_index.py. This file creates the partial index files.
Each partial index file is labeled "index\{number\}.txt".

4. Run merging.py. This file will merge the partial index files into 
one complete merged index.

5. Run query.py. You'll be prompted for input. Type in your search terms
and await the results!
