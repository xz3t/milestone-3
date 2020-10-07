import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'weeklyShopping'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

@app.route('/')
@app.route('/shopping_list')
def shopping_list():
    return render_template("shopping_list.html", lists=mongo.db.shopping_list.find())


@app.route('/items')
def items():
    return render_template("items.html", items=mongo.db.items.find())


@app.route('/add_item')
def add_item():
    return render_template("additem.html", 
        categories=mongo.db.items_categories.find(), 
        shops=mongo.db.items_shops.find(),
        units=mongo.db.items_unit.find())

@app.route('/insert_item', methods=['POST'])
def insert_item():
    items = mongo.db.items
    items.insert_one(request.form.to_dict())
    return redirect(url_for('items'))

@app.route('/edit_item/<item_id>')
def edit_item(item_id):
    the_item = mongo.db.items.find_one({"_id": ObjectId(item_id)})
    all_categories = mongo.db.items_categories.find()
    all_shops = mongo.db.items_shops.find()
    all_units = mongo.db.items_unit.find()
    return render_template('edititem.html', item=the_item,
        categories=all_categories,
        shops=all_shops,
        units=all_units)


@app.route('/recipes')
def recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())    


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)