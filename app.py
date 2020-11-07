import os
import re
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from utils import check_and_insert, check_exist

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'weeklyShopping'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)

# Index page with welcome screen and navigation menu

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

# Log In function

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {} ".format(request.form.get("username")))
                    return redirect(url_for('shopping_list'))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# Registation function

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
    return render_template("register.html")

# Shopping list managing page that displays all the items,
# users can add items, recipes/groups and remove them

@app.route('/shopping_list')
def shopping_list():
    return render_template("shopping_list.html", lists=mongo.db.shopping_list.find({"user": session["user"]}))



# Shopping list page to be used on shopping,
# will render shopping list that was created and aggregated arranged by shops.

@app.route('/use_shopping_list/')
def use_shopping_list():
    return render_template("use_shopping_list.html",
    aldi=mongo.db.shopping_list_temp.find({"user": session["user"], "item_shop": "ALDI"}),
    dunnes=mongo.db.shopping_list_temp.find({"user": session["user"], "item_shop": "Dunnes"}),
    lidl=mongo.db.shopping_list_temp.find({"user": session["user"], "item_shop": "LIDL"}),
    tesco=mongo.db.shopping_list_temp.find({"user": session["user"], "item_shop": "Tesco"}),
    local=mongo.db.shopping_list_temp.find({"user": session["user"], "item_shop": "Local Shop"}),
    ms=mongo.db.shopping_list_temp.find({"user": session["user"], "item_shop": "M&S"}),
    spar=mongo.db.shopping_list_temp.find({"user": session["user"], "item_shop": "Spar"}))

# Shopping list share route

@ app.route('/share_shopping_list/<user>')
def share_shopping_list(user):
    user = user
    return render_template("use_shopping_list.html",
                           aldi=mongo.db.shopping_list_temp.find(
                               {"user": user, "item_shop": "ALDI"}),
                           dunnes=mongo.db.shopping_list_temp.find(
                               {"user": user, "item_shop": "Dunnes"}),
                           lidl=mongo.db.shopping_list_temp.find(
                               {"user": user, "item_shop": "LIDL"}),
                           tesco=mongo.db.shopping_list_temp.find(
                               {"user": user, "item_shop": "Tesco"}),
                           local=mongo.db.shopping_list_temp.find(
                               {"user": user, "item_shop": "Local Shop"}),
                           ms=mongo.db.shopping_list_temp.find(
                               {"user": user, "item_shop": "M&S"}),
                           spar=mongo.db.shopping_list_temp.find({"user": user, "item_shop": "Spar"}))

# Function to create new aggregated list you will use on shopping

@app.route('/shopping_list_temp')
def shopping_list_temp():
    ''' 
    Function will iterate through all items adding them to 2 temporary list,
    one list to help and check item name,
    second list will hold all items information from what recipe is added and converted to float value added qty,
    when list is prepared we will remove all previous collection and write new one to database.
    '''
    shop_list=mongo.db.shopping_list.find({"user": session["user"]})
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

    mongo.db.shopping_list_temp.remove({"user": session["user"]})
    mongo.db.shopping_list_temp.insert_many(shop_list_aggregate)

    return redirect(url_for('use_shopping_list'))


# Render page for selecting items from database and adding a qty value to the shopping list

@app.route('/add_shop_item')
def add_shop_item():
    return render_template("addshopitem.html",
        items = mongo.db.items.find(),
        )


# Insert selected item to shopping list

@app.route('/insert_shop_item/', methods=['GET','POST'])
def insert_shop_item():
    '''
    Get selected item name and fetch all information about the item from items db,
    write new item to the list and inform user with an flash message
    '''
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
        'from_recipe': "--",
        'user' : session["user"]
    })
    flash('Item added to the shopping list!')
    return redirect(url_for('shopping_list'))

# Render a page for selecting an recipe/group from database

@app.route('/add_shop_recipe')
def add_shop_recipe():
    return render_template("addshoprecipe.html",
        recipes = mongo.db.recipes.find()
        )


# Insert selected recipe/group to shopping list

@app.route('/insert_shop_recipe/', methods=['GET','POST'])
def insert_shop_recipe():
    '''
    Get recipe by name and fetch all information that recipe/group contains from recipes db,
    prepare each ingredient from recipe to same format as individual item and add to shopping list,
    check_and_insert function cheks if item exist before writing it to the list,
    having all items same format will facilitate aggregation and combining similar items.
    '''
    user = session["user"]
    selected_recipe = request.form.get('recipe_name')
    selected_recipe_get = mongo.db.recipes.find_one({"recipe_name": selected_recipe})
    item1_name = selected_recipe_get["recipe_ingredient_1"]
    item2_name = selected_recipe_get["recipe_ingredient_2"]
    item3_name = selected_recipe_get["recipe_ingredient_3"]
    item4_name = selected_recipe_get["recipe_ingredient_4"]
    item5_name = selected_recipe_get["recipe_ingredient_5"]
    mongo_path = mongo.db
    check_and_insert(item1_name, user, selected_recipe, mongo_path)
    check_and_insert(item2_name, user, selected_recipe, mongo_path)
    check_and_insert(item3_name, user, selected_recipe, mongo_path)
    check_and_insert(item4_name, user, selected_recipe, mongo_path)
    check_and_insert(item5_name, user, selected_recipe, mongo_path)
    flash('All items from selected recipe added to the list!')
    return redirect(url_for('shopping_list'))


# Function will delete selected item

@app.route('/delete_shoping_item/<list_id>')
def delete_shoping_item(list_id):
    '''
    Check if item is added from items or a recipe/group,
    if item is individual remove and inform user,
    if item is part of recipe user will select if he want to delete just selected item or all recipe item is part off.
    '''
    del_all = request.args.get('del_all')
    item = mongo.db.shopping_list.find_one({'_id': ObjectId(list_id)})
    if item['from_recipe'] == "--":
        mongo.db.shopping_list.remove({'_id': ObjectId(list_id)})
        flash('Item successfully removed!')
    elif del_all == "1":
        mongo.db.shopping_list.remove({"user": session["user"], 'from_recipe': item['from_recipe']})
        flash('All items associated with recipe removed!')
    else:
        mongo.db.shopping_list.remove({'_id': ObjectId(list_id)})
        flash('selected item successfully removed!')
    return redirect(url_for('shopping_list'))


# Render page with all items in database

@app.route('/items')
def items():
    return render_template("items.html", items=mongo.db.items.find().sort("item_name"))


# Render add item page with dropdowns to help and guide user to input correct information

@app.route('/add_item')
def add_item():
    return render_template("additem.html", 
        categories=mongo.db.items_categories.find(), 
        shops=mongo.db.items_shops.find(),
        units=mongo.db.items_unit.find())


# Function to insert an item

@app.route('/insert_item', methods=['POST'])
def insert_item():
    '''
    Get the entered name and search for it ignoring case to avoid similar item name to be inputted,
    inform user if item exist with a flash mesage and reload add_item page,
    if item don't exist add it to database and inform user with flash message about success
    '''
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


# Render edit item page by id of selected item

@app.route('/edit_item/<item_id>')
def edit_item(item_id):
    '''
    Get item by id and display all info about selected item in name field and dropdown menus,
    with all other options available in the dropdowns to make a change.
    '''
    the_item = mongo.db.items.find_one({"_id": ObjectId(item_id)})
    all_categories = mongo.db.items_categories.find()
    all_shops = mongo.db.items_shops.find()
    all_units = mongo.db.items_unit.find()
    return render_template('edititem.html', item=the_item,
        categories=all_categories,
        shops=all_shops,
        units=all_units)


# Function to update an item

@app.route('/update_item/<item_id>', methods=["POST"])
def update_item(item_id):
    '''
    Update selected item by id with new provided information,
    return a flash message to user with success
    '''
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


# Render page with all recipes/groups in database

@app.route('/recipes')
def recipes():
    return render_template("recipes.html", 
        recipes=mongo.db.recipes.find().sort("recipe_name"))    


# Render the page where user will create name for his recipe/group

@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html")    


# Render edit recipe/group page by id for selected recipe

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    '''
    Get data by selected id and render a page with 5 dropdown menu containing all items in db,
    item are displayed sorted to easier navigate thru them when selecting
    '''    
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


# Function to insert an recipe

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    '''
    Will create a new recipe, return a flash message to user with
    success and further instructions to add items in created recipe
    '''
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    flash('Recipe created successfully! Edit your new recipe to add items.')
    return redirect(url_for('recipes'))


# Function to update an recipe

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    '''
    Prep 5 input dropdown menus for user to select items from db and add qty for each,
    fetch item_unit for each selected unit,
    to avoid errors had to add validation if selected item is not selected to add an empty string,
    update recipe by id and return a success flash message 
    '''
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
    item1_unit = check_exist(find_selected_item)
    item2_unit = check_exist(find_selected_item_2)
    item3_unit = check_exist(find_selected_item_3)
    item4_unit = check_exist(find_selected_item_4)
    item5_unit = check_exist(find_selected_item_5)
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
    flash('Recipe updated successfully!')
    return redirect(url_for('recipes'))


# Function to delete an recipe by id

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    flash('Recipe deleted successfully!')
    return redirect(url_for('recipes'))


# Render Feedback page

@app.route('/feedback')
def feedback():
    return render_template("feedback.html",
    feedback = mongo.db.feedback.find())


# Function to submit feedback and return flash success message

@app.route('/submit_feedback', methods=["POST"])
def submit_feedback():
    feedback = mongo.db.feedback
    feedback.insert_one(request.form.to_dict())
    flash('Your feedback is submitted. Thank you!')
    return redirect(url_for('feedback'))


# Function to log out user and remove cookie
@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)