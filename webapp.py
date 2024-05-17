from flask import Flask, render_template, request
from templates import *

app = Flask(__name__)


# example submit
@app.route('/submit_form', methods=['GET', 'POST'])
def submit():
    if request.method == "POST":
        value = ''
        data = request.form['ask']
        print("--- Received POST ---")
        print(data)
        sample = 'aaa'
        return render_template("index.html", SAMPLE_DATA=sample)


@app.route('/', methods=['GET', 'POST'])
def index():
    sample = ''
    if request.method == "POST":
        print("--- Received POST ---")
        data = request.form['ask']
        print(data)
        sample = data
    return render_template("index.html", SAMPLE_DATA=sample)


if __name__ == "__main__":
    app.run(debug=True)
