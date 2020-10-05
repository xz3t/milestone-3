import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'weeklyShopping'
app.config["MONGO_URI"] = 'mongodb+srv://root:l3tm3in@myfirstcluster.kmobf.mongodb.net/weeklyShopping?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
@app.route('/shopping_list')
def shopping_list():
    return render_template("shopping_list.html", lists=mongo.db.shopping_list.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)