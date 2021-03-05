from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        query = request.form["query"]
        
        
        url = parse.load_bin("url.bin")
        doc = parse.load_bin("doc.bin")
        index_index = parse.load_bin("index_index.bin")
        merged_index = open("merged_index.txt", "r")


        
        return render_template("results.html", query=query)
    else:
        return render_template("index.html")