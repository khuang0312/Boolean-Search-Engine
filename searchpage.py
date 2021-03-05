from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        print("YES")
    return render_template("index.html")