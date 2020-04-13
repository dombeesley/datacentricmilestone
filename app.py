import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'data_centric_books'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@myfirstcluster-mtbzq.mongodb.net/data_centric_books?retryWrites=true&w=majority'


mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/addbook')
def addbook():
    return render_template('addbook.html')


@app.route('/insert_book', methods=['POST'])
def insert_book():
    library = mongo.db.library
    library.insert_one(request.form.to_dict())
    return redirect(url_for('see_library'))


@app.route('/library')
def see_library():
    return render_template('library.html', library=mongo.db.library.find())


@app.route('/view_book/<book_id>')
def view_book(book_id):
    the_book = mongo.db.library.find_one({"_id": ObjectId(book_id)})
    return render_template('viewbook.html', book=the_book)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)