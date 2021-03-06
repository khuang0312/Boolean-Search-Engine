from flask import Flask, render_template, request
import parse
import query

app = Flask(__name__)

# url = parse.load_bin("url.bin")
# doc = parse.load_bin("doc.bin")
# stopwords = query.load_stopwords()
# index_index = parse.load_bin("index_index.bin")
# merged_index = open("merged_index.txt", "r")

@app.route('/', methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        query_string = request.form["query"]
        k = request.form["max_results"]

        url = parse.load_bin("url.bin")
        doc = parse.load_bin("doc.bin")
        stopwords = query.load_stopwords()
        index_index = parse.load_bin("index_index.bin")
        merged_index = open("merged_index.txt", "r")

        # print(url, doc, stopwords)
        
        QUERY_TERMS = query.get_query_terms(query_string, stopwords)
        QUERY_POSTINGS = query.get_query_postings(QUERY_TERMS)
        result = query.process_query(QUERY_TERMS)
        result_urls = query.get_url_names(result)
        
        results_string = ""
        for i in query.get_k_results(result_urls, int(k)):
            results_string += "<li>{}<li>".format(url)
            
        return render_template("results.html", query_string=query_string, results_string=results_string, k=k)
    else:
        return render_template("index.html")