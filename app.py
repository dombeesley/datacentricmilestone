import os
from flask import Flask, render_template, redirect, request, url_for, session
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


@app.route('/loginpage')
def loginpage():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'username': request.form['username']})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('see_library'))

    return render_template('tryagain.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})

        if existing_user is None:
            users.insert({'username': request.form['username'], 'password': request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('home'))

        return render_template('tryagain.html')

    return render_template('register.html')


@app.route('/editreview')
def edit_review():
    return render_template('editreview.html')


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)
