# Weekly Shopping List app

[View the live project here.](http://weekly-shopping-app.herokuapp.com/)

Weekly Shopping List app's aim is to simplify weekly shopping for an household and/or easily organize a small party. 
You can add items and recipe/groups of items, snap a photo in the shop of your desired product or add an picture from your tablet or pc.
Create shopping list and share it with your designated shopper.
As each family member has his/hers own preferences, weekly shopping will not differ drastically from week to week and once all items and recipe/groups will be set up it will take a few minutes to make adjustments and edit your shopping list or create one from scratch.

![Preview](/docs/responsive.jpg)

## User Experience (UX)

### Project Goals

Shopping list app project is part of Data Centric Development module from my Full Stack Software Development studies with Code Institute. 
The scope of this milestone project is to create a fully responsive website with possibility to perform CRUD (Create, Read, Update, and Delete) operation in MongoDb, using Python and Flask micro web framework.

-   ### User stories

  
    -  As a First Time Visitor, I want to :
        * be able to easily navigate throughout the site
        * have an personal space that i can log in using id and password
        * create new items with additional data a categories and preferred shops
        * create an recipe or group of usual products to simplify building the shopping list
        * add and view images for each item to help me or shopper to choice the correct item
        * view shopping list by shops and categories
        * share the shopping list
        * have a feedback or contact with developer for suggestion and reporting errors
     
    -  As a Returning Visitor, I want to :
        * be able to access saved items and recipes
        * re-use previous shopping list
        * change any item details as preferred shop or category

 

-   ### Design
    -   #### Color Scheme
        -   I opted for a white background with black text, dark blue-grey color used for buttons, navigation and footer for a clean and minimalist look.
    -   #### Typography
        -   Roboto font is used that is the default font from Materialize CSS Framework.
    -   #### Imagery
        -   Logo and icon is simple and clean, was taken from [Link](https://icons8.com/icons/set/cart)
        -   Images for base number of items and logo's for "Preferred Shop" where taken from ALDI/LIDL/Tesco web sites.

*   ### Wireframes

    -   Main, shopping list - [View](/docs/main_shopping.jpg)

    -   Items, recipes - [View](/docs/items_recipes.jpg)

    -   Mobile navigation - [View](/docs/mobile_nav.jpg)

    -   Collection structure - [View](/docs/collection.jpg)


## Features

### Main page
- Welcome page with a quick greeting message and Register and LogIn links.
- After user is logged in button Login and Register will dissapear.

### Navigation bar
- Before user will log in will display: Home , Log In and Register.
- After user has logged in will have access to the rest of the menu links.

### Footer
- Contain a short description and links to Feedback and GitHub page with the project.

### Register (Create)
- Form on the page allows user to register an account with username/password that will get created in database with condition username is not already taken.
- User will receive an flash message if user is already taken.

### Log In (Read)
- Form on the page allows user to log in into earlier created account.
- User will receive an flash message if user and/or password will not match user in database.
- After log in user will be redirected to "Manage Shopping List" section and greeted by username used on login.

### Items (Read)
- This section is a list off all items in the database sorted in alphabetically.
- User can create new Item or Edit an existing one.

### Add Item (Create, Read)
In this section user is presented with: 
- an text input for a name 
- 3 dropdown menus that are populated with predefined choices from database.(Category, UOM, Proffered Shop)
- Add Photo feature implemented with imgBB API - image can be uploaded from a local source, from mobile device can be snapped with camera. 
- cancel button to return to Items section
Item name can be entered in any case as it will be searched in database with IGNORECASE.
User will receive an flash message if name is already used, when successful user will be redirected back to Items section with a success message.

### Edit Item (Read, Update)
- Section inherits Add Item structure and functionality.
- On submit Item will be overwritten with updated information into database.
- User will receive an flash message with success and will be redirected back to Items section.

### Recipe (Read, Delete)
This section is a list with all recipes in the database sorted alphabetically.
User is presented with :
- add recipe/group button that will redirect to Add Recipe/Group section
- recipes/groups in format of an collapsible for each recipe that includes a name in the header and up to 5 items in the body with additional information.
- edit button that will redirect user to Edit Recipe/Group section.
- delete button to remove recipe/group

### Add Recipe/Group of products (Create)
- This section allows user to create a name for recipe/group with further instruction to edit it in order to add items.
- User will receive an flash message in if name already exist and will stay on same page,
when name will unique and successfully created user will be redirected to Recipes section and receive a flash message with instruction to edit created recipe/group in order to add items.

### Edit Recipe/Group of products (Read, Update)
User is presented with:
- an text input with the recipe/group name
- 5 dropdown menus that have all items with UOM from database available and sorted alphabetically for easy to access.
- each of 5 dropdown menus has a additional field for QTY input.
- Add Photo feature implemented with imgBB API - image can be uploaded from a local source, from mobile device can be snapped with camera. 
- cancel button to return to Recipes section

### Manage Shopping List (Read, Delete)
User is presented with:
- "add item" to shopping list button will redirect to Add shop item section
- "add recipe/group" to shopping list button will redirect to Add shop recipe section
- "use shopping list" button will run an aggregate function and redirect to Saved Shopping List section
- "share" will slide up a modal with a button to copy, link that can be shared for created shopping list in read only.
- list of all Items added as individual items and recipe/groups in form of collapsible with Name/Qty/Uom in header and additional information in the body
- delete button: 
        - if item is added as individual will be removed on click of the button,
        - if item was added as part of recipe/group user will be promoted with a modal and option to remove just selected item or all recipe/group it is part of.

### Saved Shopping List (Read)
User is presented with:
- "share" button will slide up a modal with a button to copy, link that can be shared for created shopping list in read-only.
- list of all Items sorted by shops
- for each shop there is a category button with jquery filter by categories if item list will get too big can be handy to have.
- items can be clicked on to strike out items that where both
- items have their appointed images from items database can be clicked on to view full screen.


### Feedback (Create, Read)
User is presented with:
- feedback form that contains name/email and feedback message
- on the bottom are displayed feedback messages except email information.

## Collections Data Structure

#### users

| _Key in DB_     | _Data type_ |
| --------------- | ----------- |
| \_id            | ObjectId    |
| username        | string      |
| password        | string      |


#### items

| _Key in DB_     | _Data type_ |
| --------------- | ----------- |
| \_id            | ObjectId    |
| item_name       | string      |
| item_category   | string      |
| item_shop       | string      |
| item_unit       | string      |
| item_img        | string      |


#### items_categories

| _Key in DB_     | _Data type_ |
| --------------- | ----------- |
| \_id            | ObjectId    |
| category_name   | string      |


#### items_shops

| _Key in DB_     | _Data type_ |
| --------------- | ----------- |
| \_id            | ObjectId    |
| shop_name       | string      |
| shop_logo       | string      |


#### items_unit

| _Key in DB_     | _Data type_ |
| --------------- | ----------- |
| \_id            | ObjectId    |
| unit            | string      |


#### recipes

| _Key in DB_              | _Data type_ |
| ------------------------ | ----------- |
| \_id                     | ObjectId    |
| recipe_name              | string      |
| recipe_ingredient_1      | string      |
| recipe_ingredient_1_qty  | string      |
| recipe_ingredient_1_unit | string      |
| recipe_ingredient_2      | string      |
| recipe_ingredient_2_qty  | string      |
| recipe_ingredient_2_unit | string      |
| recipe_ingredient_3      | string      |
| recipe_ingredient_3_qty  | string      |
| recipe_ingredient_3_unit | string      |
| recipe_ingredient_4      | string      |
| recipe_ingredient_4_qty  | string      |
| recipe_ingredient_4_unit | string      |
| recipe_ingredient_5      | string      |
| recipe_ingredient_5_qty  | string      |
| recipe_ingredient_5_unit | string      |
| recipe_img               | string      |


#### shopping_list

| _Key in DB_     | _Data type_ |
| --------------- | ----------- |
| \_id            | ObjectId    |
| item_name       | string      |
| item_unit       | string      |
| item_qty        | string      |
| item_shop       | string      |
| item_category   | string      |
| item_img        | string      |
| from_recipe     | string      |
| user            | string      |


#### shopping_list_temp

| _Key in DB_     | _Data type_ |
| --------------- | ----------- |
| \_id            | ObjectId    |
| item_name       | string      |
| item_unit       | string      |
| item_qty        | string      |
| item_shop       | string      |
| item_category   | string      |
| item_img        | string      |
| from_recipe     | string      |
| user            | string      |


#### feedback

| _Key in DB_     | _Data type_ |
| --------------- | ----------- |
| \_id            | ObjectId    |
| name            | string      |
| email           | string      |
| fmessage        | string      |


## Technologies Used

-   [HTML5](https://en.wikipedia.org/wiki/HTML5)
-   [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
-   [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
-   [Python](https://en.wikipedia.org/wiki/Python_(programming_language))
-   [MongoDB](https://en.wikipedia.org/wiki/MongoDB)

### Frameworks, Libraries & Programs Used

1. [Git](https://git-scm.com/)
    - Git was used for version control by utilizing the Gitpod terminal to commit to Git and Push to GitHub.
2. [GitHub:](https://github.com/)
    - GitHub is used to store the projects code after being pushed from Git.
3. [Materialize](https://materializecss.com/about.html)
    - Created by Google, Material Design is a design language that combines the classic principles of successful design along with innovation and technology.
4. [imgBB API:](https://api.imgbb.com/)
    - Imgbb's API allows to upload pictures to host on the server.
5. [Font Awesome:](https://fontawesome.com/)
    - Font Awesome was used on all pages throughout the website to add icons for aesthetic and UX purposes.
6. [JQuery](https://en.wikipedia.org/wiki/JQuery)
    - JavaScript library designed to simplify HTML DOM tree traversal and manipulation, event handling, css animation.
7. [Flask](https://en.wikipedia.org/wiki/Flask_(web_framework))
    - Flask is a micro web framework written in Python.
8. [Jinja](https://en.wikipedia.org/wiki/Jinja_(template_engine))
    - Jinja web template engine for the Python programming language
9. [Heroku](https://en.wikipedia.org/wiki/Heroku)
    - Heroku is a cloud platform as a service (PaaS) supporting several programming languages, including Python used in this project.


## Testing

The W3C Markup Validator, W3C CSS Validator and PEP8 Validator were used to validate code in the pages listed below to ensure there were no syntax errors in the project.

-   [W3C Markup Validator](https://validator.w3.org/) 
        - [Result - Main](https://validator.w3.org/nu/?doc=http%3A%2F%2Fweekly-shopping-app.herokuapp.com%2F)
        - [Result - Login](https://validator.w3.org/nu/?doc=http%3A%2F%2Fweekly-shopping-app.herokuapp.com%2Flogin)
        - [Result - Register](https://validator.w3.org/nu/?doc=http%3A%2F%2Fweekly-shopping-app.herokuapp.com%2Fregister)
        - [Result - Shared recipe](https://validator.w3.org/nu/?doc=http%3A%2F%2Fweekly-shopping-app.herokuapp.com%2Fshare_shopping_list%2Ftest1)
        - [Result - Feedback](https://validator.w3.org/nu/?doc=http%3A%2F%2Fweekly-shopping-app.herokuapp.com%2Ffeedback)
-   [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) - [Results](https://jigsaw.w3.org/css-validator/validator?uri=http%3A%2F%2Fweekly-shopping-app.herokuapp.com%2Fstatic%2Fcss%2Fstyle.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)
-   [PEP8 Validator](http://pep8online.com/) - app.py and utils.py - Pass

### Features Testing

#### Main page
- Check if links are working properly on navbar and main page and mobile view.
- When user is logged in SingUp message and Login and Register buttons should dissapear.

#### Register
- Check if links are working properly on navbar and main page and mobile view.
- Was register page rendered?
- Submit empty form should return an error.
- Fill in less then 5 characters, system should return error to match requested format.
- If username already exist, system should return message to the user to try again.
- When registration is a success user should be informed and redirected to LogIn page .

#### Log in
- Check if links are working properly on navbar and main page and mobile view.
- Is the Login form rendered?
- Submit empty form should return an error.
- Fill in less then 5 characters, system should return error to match requested format.
- If username and/or password doesn't match inform user with a flash message.
- When log in is a success user should be informed and redirected to manage shopping list page.

#### Manage Shopping List
- Check if links are working properly on navbar and mobile view.
- Is the shopping list page rendered?
- "Add Item" on click should redirect to Add Shop Item page (addshopitem.html)
- "Add Recipe/Group" on click should redirect to Add Shop Recipe page (addshoprecipe.html)
- "Use Shopping List" on click should aggregate created list and redirect to Saved Shopping List page (use_shopping_list.html)
- "Share" on click should reveal modal with click to clipboard functionality.
- Displayed items should have same format and displayed in collapsible format.
- "Del" on click should remove item added from items and inform user with a message, for items added from recipe/group should reveal a modal with options to delete item or all recipe/group this item is a part off.

##### Add shop item
- Page should render a form with dropdown menu with all items in database.
- Item/Ingredient and Quantity fields should have required attribute to avoid adding empty items.
- "Add item" on click should submit form and redirect back to Manage Shopping List page with a message to inform action was a success.
- "Cancel" on click should return to Manage Shopping List.

##### Add shop recipe
- Page should render a form with dropdown menu with all recipes in database.
- Recipe field should have required attribute to avoid empty submit.
- "Add Recipe/Group" on click should submit form, add each item from recipe individually with addition of recipe name then redirect back to Manage Shopping List page with a message to inform action was a success.
- "Cancel" on click should return to Manage Shopping List.

#### Use Shopping List
- Should render aggregated version of Manage Shopping List.
- "Share" on click should reveal modal with click to clipboard functionality.
- Shops that does not have an item in the list should be hidden.
- All items should be displayed grouped by preferred shop.
- "Category" button should reveal a horizontal scrolling list (in mobile view) that allow you to show just selected category of products.
- On click on items text should have an strike effect to highlight that item is both.
- Each item should have a thumb image that was assigned to it in database, on click should show a full screen picture.

#### Items
- Check if links are working properly on navbar and mobile view.
- Should render Items page in a collapsible format with name and image in the header and additional information in the body.
- "Add Item" on click should redirect to Add Item page and inform user with a message.
- "Edit" on click should redirect to Edit Item page.

##### Add Items
- Should render a form with Item name, 3 dropdown menus and an file input.
- Dropdown menus should read information from database and display information correctly.
- Name and dropdown selectable fields should have required attributes.
- "Add Photo" should run set-up Script in background that connects to imgBB API and upload image to the server returning link for the image in text input beside it.
- "Add Item" on click should check if name already exist and return a message to the user, if it is a success should return to Items page.
- "Cancel" on click should return to Item Page

##### Edit Item
- Inherits add item functionality, let user update all the fields.
- Should display all information about selected item in the form.
- "Edit Item" will submit new information to database and redirect user to Items page with a success message.

#### Recipes
- Check if links are working properly on navbar and mobile view.
- Should render Items page in a collapsible format with name and image in the header and list of items with additional information in the body.
- Should not show empty items in recipe in collapsible body.
- "Add Recipe/Group" on click should redirect to Add Recipe page.
- "Edit" on click should redirect to Edit Recipe/Group page.
- "Delete" on click will delete recipe from the list reloading the page and informing user with a flash message.

##### Add Recipe/Group
- Should render a page with form containing a text input for the name of Recipe/Group.
- User have a short tip with further instructions after assigning a name.
- Field is set as required to avoid empty entry.
- "Create recipe" on click will submit the form and redirect user to Recipes page with a flash message with instruction to edit item to add ingredients.
- "Cancel" on click should return to Recipe Page.

##### Edit recipe
- Should render a form with Recipe name, 5 dropdown menus with Qty for each item and an file input.
- Dropdown should pull data from Items database and display information correctly.
- "Edit Recipe" on click will submit form and update database information.
- "Cancel" on click should return to Recipe Page.

#### Feedback
- Check if links are working properly on navbar, footer and mobile view.
- Should render a form in first part of the page and submitted feedback messages on the bottom.
- All fields should have required attribute.
- Email field should have correct email format on submit.
- "Send" will submit form and reload the page with a success message, with users message loaded as last one on the page.

#### Log Out
- Check if links are working properly on navbar and mobile view.
- Should end session and redirect to Main Page with a flash message to the user.


### Further Testing

-   The Website was tested on Google Chrome, Opera, Microsoft Edge, and mobile Safari browsers.
-   The website was viewed on a variety of devices such as Desktop, Laptop, iPhone5S, iPhone 6, Nokia 5 & Pixel3a.
-   Friends were asked to review functionality and point out any bugs and/or user experience issues.


### Known Bugs

- materialbox don't work properly on saved shopping list, some images will not open in full screen. Works in the top section of the page. on scroll down to the bottom images doesnt work.
- materialize selectable on chrome some time need to click twice, no issue on mobile version.

### Features to implement

- Add on main page total registered users and items/recipes in database.
- In Items and Recipes on "Add photo" add a delay in form of loader so user don't click on submit form before imgBB will receive response and fill in with correct link.
- In Saved Shopping list, move marked as bought items to bottom of the page or hide when marked.
- Add search function to items and recipes

## Deployment

### Heroku with Github integration

1. Create a Procfile with the terminal command echo web: python app.py > Procfile.
2. Create a requirements.txt: pip3 freeze --local > requirements.txt.
3. Push and commit requirements.txt and Procfile
4. On the Heroku app page, click on the Deploy, find Deployment method and select GitHub
5. In search for repository to connect to select desired repo-name and link it to Heroku.
6. On the Heroku app page, click on Settings -> Reveal Config Vars
7. Set the Config Vars in the Settings: 
    - Debug: False; 
    - IP: 0.0.0.0; 
    - PORT: 5000;
    - MONGO_URI: mongodb+srv://username:password@myfirstcluster.kmobf.mongodb.net/weeklyShopping?retryWrites=true&w=majority;
    - SECRET_KEY: <your_secret_key>.
8. Navigate back Deploy section, click on the Deploy Branch, you can enable Automatic Deploy, in automatic mode every push to GitHub wil automatically the latest version.
9. Now app is deployed on Heroku, you can open and view it by clicking on the Open app on top of the page.


    
### Media

-   Pictures for items were taken from LIDL/ALDI/Tesco websites.
-   Logo and icon [Link](https://icons8.com/icons/set/cart)
-   Main page image [Link](https://pixabay.com/photos/grocery-list-pen-paper-notepad-1670408/)

### Acknowledgements

-   My Mentor for continuous constructive feedback.


### Links

- Responsive image [Link](http://ami.responsivedesign.is/)
