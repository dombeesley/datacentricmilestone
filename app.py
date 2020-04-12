import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'data_centric_books'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@myfirstcluster-mtbzq.mongodb.net/test?retryWrites=true&w=majority'


mongo = PyMongo(app)



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/addbook')
def addbook():
    return render_template('addbook.html')


@app.route('/library')
def library():
    return render_template('library.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)