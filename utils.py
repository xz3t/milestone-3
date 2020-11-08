def check_and_insert(item_name, user, selected_recipe, mongo_path):
    """
    Check if items exist if false = none, if true = prepare item and
    insert to db
    """
    selected_recipe_get = mongo_path.recipes.find_one(
        {"recipe_name": selected_recipe})
    find_selected_item = mongo_path.items.find_one({"item_name": item_name})
    recipesop = mongo_path.shopping_list
    if find_selected_item is None:
        item = "none"
    else:
        item_unit = find_selected_item["item_unit"]
        item_qty = selected_recipe_get["recipe_ingredient_1_qty"]
        item_shop = find_selected_item["item_shop"]
        item_category = find_selected_item["item_category"]
        item_img = find_selected_item["item_img"]
        recipesop.insert_one({
            'item_name': item_name,
            'item_unit': item_unit,
            'item_qty': item_qty,
            'item_shop': item_shop,
            'item_category': item_category,
            'item_img': item_img,
            'from_recipe': selected_recipe,
            'user': user
        })


def check_exist(item):
    """
    Check if item exist if none return "" if value exist return the value
    """
    if item is None:
        return " "
    else:
        return item["item_unit"]
