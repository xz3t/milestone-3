import os
import re
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'weeklyShopping'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/shopping_list')
def shopping_list():
    return render_template("shopping_list.html", lists=mongo.db.shopping_list.find())


@app.route('/use_shopping_list')
def use_shopping_list():
    return render_template("use_shopping_list.html",
    aldi=mongo.db.shopping_list_temp.find({"item_shop": "ALDI"}),
    dunnes=mongo.db.shopping_list_temp.find({"item_shop": "Dunnes"}),
    lidl=mongo.db.shopping_list_temp.find({"item_shop": "LIDL"}),
    tesco=mongo.db.shopping_list_temp.find({"item_shop": "Tesco"}),
    local=mongo.db.shopping_list_temp.find({"item_shop": "Local Shop"}),
    ms=mongo.db.shopping_list_temp.find({"item_shop": "M&S"}),
    spar=mongo.db.shopping_list_temp.find({"item_shop": "Spar"}))


@app.route('/shopping_list_temp')
def shopping_list_temp():
    shop_list=mongo.db.shopping_list.find()
    shop_list_aggregate = []
    shop_list_aggregate_key = []
    for item in shop_list:
        key = item["item_name"]
        if key in shop_list_aggregate_key:
            for item_agg in shop_list_aggregate:
                if item_agg["item_name"] == key:
                    item_agg["item_qty"] = float(item_agg["item_qty"]) + float(item["item_qty"])
                    item_agg["from_recipe"] = item_agg["from_recipe"] + ", " + item["from_recipe"]
        else:
            shop_list_aggregate.append(item)
            shop_list_aggregate_key.append(item["item_name"])

    mongo.db.shopping_list_temp.drop()
    mongo.db.shopping_list_temp.insert_many(shop_list_aggregate)

    return redirect(url_for('use_shopping_list'))


@app.route('/add_shop_item')
def add_shop_item():
    return render_template("addshopitem.html",
        items = mongo.db.items.find(),
        )


@app.route('/insert_shop_item/', methods=['GET','POST'])
def insert_shop_item():
    selected_item = request.form.get('item_name')
    find_selected = mongo.db.items.find_one({"item_name": selected_item})
    item_shop = find_selected["item_shop"]
    item_category = find_selected["item_category"]
    item_unit = find_selected["item_unit"]
    item_img = find_selected["item_img"]
    itemsop = mongo.db.shopping_list
    itemsop.insert_one( 
    {
        'item_name':request.form.get('item_name'), 
        'item_unit':item_unit,
        'item_qty':request.form.get('item_qty'),
        'item_shop':item_shop,
        'item_category':item_category,
        'item_img':item_img,
        'from_recipe': "--"
    })
    flash('Item added to the shopping list!')
    return redirect(url_for('shopping_list'))

@app.route('/add_shop_recipe')
def add_shop_recipe():
    return render_template("addshoprecipe.html",
        recipes = mongo.db.recipes.find()
        )


@app.route('/insert_shop_recipe/', methods=['GET','POST'])
def insert_shop_recipe():
    selected_recipe = request.form.get('recipe_name')
    selected_recipe_get = mongo.db.recipes.find_one({"recipe_name": selected_recipe})
    item1_name = selected_recipe_get["recipe_ingredient_1"]
    item2_name = selected_recipe_get["recipe_ingredient_2"]
    item3_name = selected_recipe_get["recipe_ingredient_3"]
    item4_name = selected_recipe_get["recipe_ingredient_4"]
    item5_name = selected_recipe_get["recipe_ingredient_5"]
    find_selected_item = mongo.db.items.find_one({"item_name": item1_name})
    find_selected_item_2 = mongo.db.items.find_one({"item_name": item2_name})
    find_selected_item_3 = mongo.db.items.find_one({"item_name": item3_name})
    find_selected_item_4 = mongo.db.items.find_one({"item_name": item4_name})
    find_selected_item_5 = mongo.db.items.find_one({"item_name": item5_name})
    item1_unit = find_selected_item["item_unit"]
    item2_unit = find_selected_item_2["item_unit"]
    item3_unit = find_selected_item_3["item_unit"]
    item4_unit = find_selected_item_4["item_unit"]
    item5_unit = find_selected_item_5["item_unit"]
    item1_qty = selected_recipe_get["recipe_ingredient_1_qty"]
    item2_qty = selected_recipe_get["recipe_ingredient_2_qty"]
    item3_qty = selected_recipe_get["recipe_ingredient_3_qty"]
    item4_qty = selected_recipe_get["recipe_ingredient_4_qty"]
    item5_qty = selected_recipe_get["recipe_ingredient_5_qty"]
    item1_shop = find_selected_item["item_shop"]
    item2_shop = find_selected_item_2["item_shop"]
    item3_shop = find_selected_item_3["item_shop"]
    item4_shop = find_selected_item_4["item_shop"]
    item5_shop = find_selected_item_5["item_shop"]
    item1_category = find_selected_item["item_category"]
    item2_category = find_selected_item_2["item_category"]
    item3_category = find_selected_item_3["item_category"]
    item4_category = find_selected_item_4["item_category"]
    item5_category = find_selected_item_5["item_category"]
    item1_img = find_selected_item["item_img"]
    item2_img = find_selected_item_2["item_img"]
    item3_img = find_selected_item_3["item_img"]
    item4_img = find_selected_item_4["item_img"]
    item5_img = find_selected_item_5["item_img"]
    recipesop = mongo.db.shopping_list
    recipesop.insert_many( [
    {
        'item_name':item1_name, 
        'item_unit':item1_unit, 
        'item_qty':item1_qty,
        'item_shop':item1_shop,
        'item_category':item1_category,
        'item_img':item1_img,
        'from_recipe': selected_recipe
    },
     {
        'item_name':item2_name, 
        'item_unit':item2_unit, 
        'item_qty':item2_qty,
        'item_shop':item2_shop,
        'item_category':item2_category,
        'item_img':item2_img,
        'from_recipe': selected_recipe
    },
     {
        'item_name':item3_name, 
        'item_unit':item3_unit, 
        'item_qty':item3_qty,
        'item_shop':item3_shop,
        'item_category':item3_category,
        'item_img':item3_img,
        'from_recipe': selected_recipe
    },
     {
        'item_name':item4_name, 
        'item_unit':item4_unit, 
        'item_qty':item4_qty,
        'item_shop':item4_shop,
        'item_category':item4_category,
        'item_img':item4_img,
        'from_recipe': selected_recipe
    },
     {
        'item_name':item5_name, 
        'item_unit':item5_unit, 
        'item_qty':item5_qty,
        'item_shop':item5_shop,
        'item_category':item5_category,
        'item_img':item5_img,
        'from_recipe': selected_recipe
    }
    ])
    flash('All items from selected recipe added to the list!')
    return redirect(url_for('shopping_list'))


@app.route('/delete_shoping_item/<list_id>')
def delete_shoping_item(list_id):
    item = mongo.db.shopping_list.find_one({'_id': ObjectId(list_id)})
    if item['from_recipe'] == "--":
        mongo.db.shopping_list.remove({'_id': ObjectId(list_id)})
        flash('Item successfully removed!')
    else :
        mongo.db.shopping_list.remove({'from_recipe': item['from_recipe']})
        flash('All items associated with recipe removed!') 
    return redirect(url_for('shopping_list'))


@app.route('/items')
def items():
    return render_template("items.html", items=mongo.db.items.find().sort("item_name"))


@app.route('/add_item')
def add_item():
    return render_template("additem.html", 
        categories=mongo.db.items_categories.find(), 
        shops=mongo.db.items_shops.find(),
        units=mongo.db.items_unit.find())


@app.route('/insert_item', methods=['POST'])
def insert_item():
    error = None
    items = mongo.db.items
    item_name = request.form.get('item_name')
    exist = mongo.db.items.find_one({"item_name": re.compile(item_name, re.IGNORECASE)})
    if exist is None:
        flash('Item successfully added!')
        items.insert_one(request.form.to_dict())
        return redirect(url_for('items'))
    else:
        error = 'Item with this name is already in database. please choice another name or edit existing item.'
    return render_template("additem.html", error=error, categories=mongo.db.items_categories.find(), shops=mongo.db.items_shops.find(), units=mongo.db.items_unit.find())


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
    flash('Item updated successfully!')
    return redirect(url_for('items'))


@app.route('/recipes')
def recipes():
    return render_template("recipes.html", 
        recipes=mongo.db.recipes.find().sort("recipe_name"))    


@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html")    


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_item1 = mongo.db.items.find()
    the_item2 = mongo.db.items.find()
    the_item3 = mongo.db.items.find()
    the_item4 = mongo.db.items.find()
    the_item5 = mongo.db.items.find()
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('editrecipe.html', 
            recipe=the_recipe,
            item1=the_item1.sort("item_name"),
            item2=the_item2.sort("item_name"),
            item3=the_item3.sort("item_name"),
            item4=the_item4.sort("item_name"),
            item5=the_item5.sort("item_name"))


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    flash('Recipe created successfully! Edit your new recipe to add items.')
    return redirect(url_for('recipes'))


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    item1_name = request.form.get('recipe_ingredient_1')
    item2_name = request.form.get('recipe_ingredient_2')
    item3_name = request.form.get('recipe_ingredient_3')
    item4_name = request.form.get('recipe_ingredient_4')
    item5_name = request.form.get('recipe_ingredient_5')
    find_selected_item = mongo.db.items.find_one({"item_name": item1_name})
    find_selected_item_2 = mongo.db.items.find_one({"item_name": item2_name})
    find_selected_item_3 = mongo.db.items.find_one({"item_name": item3_name})
    find_selected_item_4 = mongo.db.items.find_one({"item_name": item4_name})
    find_selected_item_5 = mongo.db.items.find_one({"item_name": item5_name})
    if find_selected_item is None:
        item1_unit = ""
    else:
        item1_unit = find_selected_item["item_unit"]    
    if find_selected_item_2 is None:
        item2_unit = ""
    else:
        item2_unit = find_selected_item_2["item_unit"] 
    if find_selected_item_3 is None:
        item3_unit = ""
    else:
        item3_unit = find_selected_item_3["item_unit"]
    if find_selected_item_4 is None:
        item4_unit = ""
    else:
        item4_unit = find_selected_item_4["item_unit"]
    if find_selected_item_5 is None:
        item5_unit = ""
    else:
        item5_unit = find_selected_item_5["item_unit"]
    recipe = mongo.db.recipes
    recipe.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'), 
        'recipe_ingredient_1':request.form.get('recipe_ingredient_1'),
        'recipe_ingredient_1_qty':request.form.get('recipe_ingredient_1_qty'),
        'recipe_ingredient_1_unit': item1_unit,
        'recipe_ingredient_2':request.form.get('recipe_ingredient_2'),
        'recipe_ingredient_2_qty':request.form.get('recipe_ingredient_2_qty'),
        'recipe_ingredient_2_unit': item2_unit,
        'recipe_ingredient_3':request.form.get('recipe_ingredient_3'),
        'recipe_ingredient_3_qty':request.form.get('recipe_ingredient_3_qty'),
        'recipe_ingredient_3_unit': item3_unit,
        'recipe_ingredient_4':request.form.get('recipe_ingredient_4'),
        'recipe_ingredient_4_qty':request.form.get('recipe_ingredient_4_qty'),
        'recipe_ingredient_4_unit': item4_unit,
        'recipe_ingredient_5':request.form.get('recipe_ingredient_5'),
        'recipe_ingredient_5_qty':request.form.get('recipe_ingredient_5_qty'),
        'recipe_ingredient_5_unit': item5_unit,
        'recipe_img':request.form.get('recipe_img'),

    })
    flash('Recipe updated successfully')
    return redirect(url_for('recipes'))


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    flash('Recipe deleted successfully!')
    return redirect(url_for('recipes'))


@app.route('/feedback')
def feedback():
    return render_template("feedback.html",
    feedback = mongo.db.feedback.find())


@app.route('/submit_feedback', methods=["POST"])
def submit_feedback():
    feedback = mongo.db.feedback
    feedback.insert_one(request.form.to_dict())
    flash('Your feedback is submitted. Thank you!')
    return redirect(url_for('feedback'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)