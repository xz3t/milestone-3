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
    recipe = mongo.db.recipes.find_one({"recipe_name" : "Pancakes"})
    ingredient = recipe["recipe_ingredient_1"]
    item_1 = mongo.db.items.find_one({"item_name": ingredient})
    shop1 = item_1["item_shop"]
    item_1_qty = recipe["recipe_ingredient_1_qty"]
    y = {
        'item_name':item_1,
        'item_shop': shop1,
        'item_qty':item_1_qty
    }

    return render_template("shopping_list.html", lists=mongo.db.shopping_list.find(), x = y)


@app.route('/add_shop_item')
def add_shop_item():
    return render_template("addshopitem.html",
        items = mongo.db.items.find(),
        units=mongo.db.items_unit.find(),
        )


@app.route('/insert_shop_item/', methods=['GET','POST'])
def insert_shop_item():
    selected_item = request.form.get('item_name')
    find_selected = mongo.db.items.find_one({"item_name": selected_item})
    item_shop = find_selected["item_shop"]
    item_category = find_selected["item_category"]
    item_img = find_selected["item_img"]
    itemsop = mongo.db.shopping_list
    itemsop.insert_one( 
    {
        'item_name':request.form.get('item_name'), 
        'item_unit':request.form.get('item_unit'), 
        'item_qty':request.form.get('item_qty'),
        'item_shop':item_shop,
        'item_category':item_category,
        'item_img':item_img,
    })
    return redirect(url_for('shopping_list'))



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


@app.route('/update_item/<item_id>', methods=["POST"])
def update_item(item_id):
    item = mongo.db.items
    item.update( {'_id': ObjectId(item_id)},
    {
        'item_name':request.form.get('item_name'),
        'item_category':request.form.get('item_category'),
        'item_shop': request.form.get('item_shop'),
        'item_unit': request.form.get('item_unit'),
        'item_img':request.form.get('item_img')
    })
    return redirect(url_for('items'))


@app.route('/recipes')
def recipes():
    return render_template("recipes.html", 
        recipes=mongo.db.recipes.find())    


@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html")    

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_item1 = mongo.db.items.find()
    the_unit1 = mongo.db.items_unit.find()
    the_item2 = mongo.db.items.find()
    the_unit2 = mongo.db.items_unit.find()
    the_item3 = mongo.db.items.find()
    the_unit3 = mongo.db.items_unit.find()
    the_item4 = mongo.db.items.find()
    the_unit4 = mongo.db.items_unit.find()
    the_item5 = mongo.db.items.find()
    the_unit5 = mongo.db.items_unit.find()
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('editrecipe.html', 
            recipe=the_recipe,
            unit1=the_unit1,
            item1=the_item1.sort("item_name"),
            unit2=the_unit2,
            item2=the_item2.sort("item_name"),
            unit3=the_unit3,
            item3=the_item3.sort("item_name"),
            unit4=the_unit4,
            item4=the_item4.sort("item_name"),
            unit5=the_unit5,
            item5=the_item5.sort("item_name"))


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('recipes'))


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipe = mongo.db.recipes
    object_item_1= mongo.db.items.find_one({"item_name": request.form.get('recipe_ingredient_1')})
    object_item_2= mongo.db.items.find_one({"item_name": request.form.get('recipe_ingredient_2')})
    object_item_3= mongo.db.items.find_one({"item_name": request.form.get('recipe_ingredient_3')})
    object_item_4= mongo.db.items.find_one({"item_name": request.form.get('recipe_ingredient_4')})
    object_item_5= mongo.db.items.find_one({"item_name": request.form.get('recipe_ingredient_5')})
    recipe.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'), 
        'recipe_ingredient_1':request.form.get('recipe_ingredient_1'),
        'recipe_ingredient_1_object':object_item_1,
        'recipe_ingredient_1_unit':request.form.get('recipe_ingredient_1_unit'),
        'recipe_ingredient_1_qty':request.form.get('recipe_ingredient_1_qty'),
        'recipe_ingredient_2':request.form.get('recipe_ingredient_2'),
        'recipe_ingredient_2_object':object_item_2,
        'recipe_ingredient_2_unit':request.form.get('recipe_ingredient_2_unit'),
        'recipe_ingredient_2_qty':request.form.get('recipe_ingredient_2_qty'),
        'recipe_ingredient_3':request.form.get('recipe_ingredient_3'),
        'recipe_ingredient_3_object':object_item_3,
        'recipe_ingredient_3_unit':request.form.get('recipe_ingredient_3_unit'),
        'recipe_ingredient_3_qty':request.form.get('recipe_ingredient_3_qty'),
        'recipe_ingredient_4':request.form.get('recipe_ingredient_4'),
        'recipe_ingredient_4_object':object_item_4,
        'recipe_ingredient_4_unit':request.form.get('recipe_ingredient_4_unit'),
        'recipe_ingredient_4_qty':request.form.get('recipe_ingredient_4_qty'),
        'recipe_ingredient_5':request.form.get('recipe_ingredient_5'),
        'recipe_ingredient_5_object':object_item_5,
        'recipe_ingredient_5_unit':request.form.get('recipe_ingredient_5_unit'),
        'recipe_ingredient_5_qty':request.form.get('recipe_ingredient_5_qty'),
        'recipe_img':request.form.get('recipe_img'),

    })
    return redirect(url_for('recipes'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)