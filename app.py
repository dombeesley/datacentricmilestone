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


@app.route('/editreview/<book_id>')
def edit_review(book_id):
    the_book = mongo.db.library.find_one({"_id": ObjectId(book_id)})
    return render_template('editreview.html', book=the_book)


@app.route('/update_review/<book_id>', methods=["POST"])
def update_review(book_id):
    library = mongo.db.library
    library.update({'_id': ObjectId(book_id)},
    {
        'title': request.form.get('task_name'),
        'author': request.form.get('task_description'),
        'date_read': request.form.get('due_date'),
        'username': request.form.get('is_urgent'),
        'genre': request.form.get('is_urgent'),
        'image': request.form.get('is_urgent'),
        'book_review': request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))


@app.route('/contemp')
def contemp():
    return render_template('genre/contemp.html', library=mongo.db.library.find())


@app.route('/crime')
def crime():
    return render_template('genre/crime.html', library=mongo.db.library.find())


@app.route('/fantasy')
def fantasy():
    return render_template('genre/fantasy.html', library=mongo.db.library.find())


@app.route('/historical')
def historical():
    return render_template('genre/historical.html', library=mongo.db.library.find())


@app.route('/horror')
def horror():
    return render_template('genre/horror.html', library=mongo.db.library.find())


@app.route('/romance')
def romance():
    return render_template('genre/romance.html', library=mongo.db.library.find())


@app.route('/scifi')
def scifi():
    return render_template('genre/scifi.html', library=mongo.db.library.find())


@app.route('/thriller')
def thriller():
    return render_template('genre/thriller.html', library=mongo.db.library.find())


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

        return render_template('sorry.html')

    return render_template('register.html')


@app.route('/logout')
def log_out():
    return render_template('logout.html')


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)
