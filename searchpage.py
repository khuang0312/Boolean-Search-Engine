from flask import Flask, render_template, request, Markup
import parse
import query

from time import perf_counter



def intersect(p1 : list, p2 : list) -> [(int, int)]:
    ''' Given two sorted (by docID) postings lists, merge them 
        together into a single list. 
        Returns list of tuples (docIDs, term freq).
        len(p1) must be less than len(p2).
        Used psudeo code form lec 15, slide 32.
        Used for AND queries
    '''
    
    result = list()

    # indices to keep track of position in posting
    i1 = 0 
    i2 = 0 
    
    while (i1 < len(p1) and i2 < len(p2)):
        posting1 = p1[i1]
        posting2 = p2[i2]

        # if the docIDs match, append to the result
        if posting1[0] == posting2[0]:
            result.append(posting1)
            i1 += 1
            i2 += 1
        elif posting1[0] < posting2[0]:
            i1 += 1
        else:
            i2 += 1

    return result


def get_query_postings(query_list : [str], merged_index, index_index) -> dict:
    ''' Returns dict mapping stemmed token to posting 
    '''
    postings = dict()
    for token in query_list:
        if token not in postings:
            postings[token] = get_postings(token, merged_index, index_index)
    return postings


def get_postings(token : str, merged_index, index_index) -> [list]:
    ''' Returns the postings of the given token 
    '''
    try:
        seek = int(index_index[token])
        merged_index.seek(seek)
        # werner [[30886, 6.258362786994808, 375, 4964, 5000], [30936, 4.236864622317388, 526]]
        line = merged_index.readline()
        return eval(line.split(" ",1)[1])
    except KeyError:
        print("Token \'{}\' not found!".format(token))

def process_query(query : [str], QUERY_POSTINGS, merged_index, index_index) -> [(int, int)]:
    ''' Assuming there are atleast two tokens to process 
        Returns list of resulting postings, sorted by frequency 
        in descending order
    '''
    result = list()
    start = perf_counter()
    # sort list of dict keys by len of the postings in descending order
    QUERY_POSTINGS = sorted(QUERY_POSTINGS, key=lambda key: len(QUERY_POSTINGS[key]))

    # get the intersections for each token
    for token in QUERY_POSTINGS:
        if len(result) == 0:
            # result.extend(get_postings)
            result.extend(get_postings(token, merged_index, index_index))
        else:
            result.extend(intersect(result, get_postings(token, merged_index, index_index)))

    # sort result by tf idf in descending order
    result = sorted(result, key = lambda posting: posting[1]+posting[2], reverse = True)
    end = perf_counter()
    print("Search time elapsed: {} ms".format( (end-start) * 1000))
    return result

def get_url_names(postings : [[int]], url) -> [str]:
    ''' Given the results {docID:scores} dict, return a list of corresponding URLs '''
    result = list()
   
    for posting in postings:
        doc_id = 0
        result.append(parse.defrag_url(url[posting[doc_id]]))
    return result


url = parse.load_bin("url.bin")
doc = parse.load_bin("doc.bin")
stopwords = query.load_stopwords()
index_index = parse.load_bin("index_index.bin")
merged_index = open("merged_index.txt", "r")
        


app = Flask(__name__)



@app.route('/', methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        query_string = request.form["query"]
        k = request.form["max_results"]

        
        

        # print(url, doc, stopwords)
        
        QUERY_TERMS = query.get_query_terms(query_string, stopwords)
        QUERY_POSTINGS = get_query_postings(QUERY_TERMS, merged_index, index_index)
        start = perf_counter()
        result = process_query(QUERY_TERMS, QUERY_POSTINGS, merged_index, index_index)
        end = perf_counter()
        result_urls = get_url_names(result, url)

        query_time = (end - start) * 1000
        
        results_string = ""
        result_set = query.get_k_results(result_urls, int(k))
        for i in result_set:
            results_string += "<li><a href={}>{}</a></li>".format(i, i)
        
            
        return render_template("results.html", query_string=query_string, results_string=Markup(results_string), k=len(result_set), query_time=query_time)
    else:
        return render_template("index.html")