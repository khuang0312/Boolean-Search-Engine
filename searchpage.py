from flask import Flask, render_template, request
import parse
import query

app = Flask(__name__)

url = parse.load_bin("url.bin")
doc = parse.load_bin("doc.bin")
index_index = parse.load_bin("index_index.bin")
merged_index = open("merged_index.txt", "r")

@app.route('/', methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        query = request.form["query"]
        
        QUERY_TERMS = query.get_query_terms(query)
        QUERY_POSTINGS = query.get_query_postings(query_list)
        result = query.process_query(QUERY_TERMS)
        result_urls = query.get_url_names(result)
        results_string = ""
        for url in urls:
            results_string += "<li>{}<li>".format(url)

        return render_template("results.html", query=query, results_string=results_string)
    else:
        return render_template("index.html")