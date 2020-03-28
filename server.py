"""Main Serverr for MHH page/app
"""


from flask import Flask, redirect, request, flash, render_template, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Project, Inventory

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar

app.secret_key = "ProtectTheHoard"

# This option will cause Jinja to throw UndefinedErrors if a value hasn't
# been defined (so it more closely mimics Python's behavior)
app.jinja_env.undefined = StrictUndefined

# This option will cause Jinja to automatically reload templates if they've been
# changed. This is a resource-intensive operation though, so it should only be
# set while debugging.
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
#app.secret_key = 'ABC'




@app.route('/')
def index():
    """Show our index page."""

    # check to see if user is logged in
    # user_id = session['user_id']

    # if user_id is None:
    #     return render_template('index.html')

    # else:
    #     return redirect(f'/user/{user_id}')

    # if not display the index page

    # if there is a user_id in session
    # display the user profile page?

    return render_template('index.html')

@app.route('/index')
def index2():
    """Show our index page."""
    user_id = session['user_id']
    # check to see if user is logged in


    # if not display the index page

    # if there is a user_id in session
    # display the user profile page?
    return render_template('index.html')

@app.route('/login_form')
def login_form():
    """Bring the User to the login webpage."""

    return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login():

    #check to see if user_id is in session


    """Validate email and password and update session."""

    user_email = request.form.get('email')
    user_password = request.form.get('password')

    

    user = User.query.filter_by(email=request.form.get('email')).first()
        
    if user.login(request.form.get('password')):
        app.logger.info('Login successful ...')
        session['user_id'] = user.user_id
        flash('Login successful.')
        return redirect(f'/user/{ user.user_id }')
    else:
        app.logger.info('Login failed!')
        return redirect('/login_form')

    


@app.route("/logout")
def process_logout():
    """Log user out."""

    del session["user_id"]
    flash("Logged out.")
    return redirect("/")


@app.route("/register")
def register():
    """Display the form for user to fill out and register for an account."""
    return render_template('register.html')


@app.route("/new_user", methods=['POST'])
def new_user():
    """Take the information from the register form and insert this User into 
    the database"""
    email = request.form["email"]
    password = request.form["password"]
    fname = request.form["fname"]
    lname= request.form["lname"]
    username = request.form["username"]

    new_user = User(username=username,
                    email=email,
                    password=password,
                    fname=fname,
                    lname=lname)

    
    #hashing password before storing it
    new_user.create_hashedpw(password)

    new_user.save()

    # db.session.add(new_user)
    # db.session.commit()

    flash(f"User {email} added.")
    return redirect("/")


@app.route('/user/<user_id>')
def user_info(user_id):
    """Display user info."""
  
    user = User.query.get(user_id)
    inventory = user.inventory
    projects = user.projects

    return render_template('user_profile.html', user=user, inventory=inventory,
                                             projects=projects)

    # # Using JSON to return user profile information
    # user = User.query.get(user_id)

    # return jsonify([user.serialize()])



@app.route('/user')
def user():
    """ NOTE TO SELF - do I NEED two routes???"""
    user_id = session['user_id']
    user = User.query.get(user_id)

    return redirect(f'/user/{user_id}')


@app.route('/add_inv', methods=['POST'])
def create_inv():
    """ Display the form for the user to enter the required info for an 
    inventory item """

    # get the user info saved in session
    user_id = session['user_id']

    #get the info from the form
    inv_name = request.form['inv_name']
    inv_type = request.form['inv_type']
    description = request.form['description']
    price = request.form['price']
    count_per_package = request.form['count_per_package']
    manufacturer = request.form['manufacturer']
    size = request.form['size']

    # Not using picture path yet - just initializing it as a blank
    picture_path=""
    # do we need to process keywords into a python list?
    keywords = request.form['keywords']

    
    #create the inv item
    new_inv = Inventory(user_id=user_id,
                        inv_name=inv_name,
                        inv_type=inv_type,
                        description=description,
                        price=price,
                        count_per_package=count_per_package,
                        manufacturer=manufacturer,
                        size=size,
                        picture_path=picture_path,
                        keywords=keywords)

    

    

    #add to session & commit
    # db.session.add(new_inv)
    # db.session.commit()
    new_inv.save()

    flash(f"Inventory Item: {inv_name} added.")

    return redirect('/inventory')


@app.route('/add_inv_form')
def add_inv_form():
    """ Add a new inventory item """
    return render_template('inv_form.html')

@app.route('/view_inv_item/<int:inv_id>')
def get_inv_item(inv_id):
    """View an individual inv_item"""

    # get the user info saved in session
    user_id = session['user_id']

    #the inv_id was passed in with the route path
    # we can use it to query the db and get an individual inventory
    # item from the inventory table.
    inv_item = Inventory.query.get(inv_id)
    
    #return that info to be displayed on the view_inv_item.html page

    return render_template("view_inv_item.html", inv_item=inv_item)

@app.route('/inventory')
def view_inventory():
    """ View all the inventory for a particular user"""

    user_id = session['user_id']
    user = User.query.get(user_id)

    inventory = user.inventory
    #get the tools for this user in the inventory table
    # utools_query = db.session.query(inventory).filter_by(inv_type='t').all()
    # usupplies_query = db.session.query(inventory).filter_by(inv_type='s').all()

    
    return render_template('inventory.html', user=user, inventory=inventory)

@app.route('/del_inv/<int:inv_id>')
def delete_inventory(inv_id):
    """Method to delete an inventory item from the database"""
    user_id = session['user_id']
    user = User.query.get(user_id)

    inv_item = Inventory.query.get(inv_id)
    #inv_item = Inventory.query.filter(int(inv_id))

    #get info from the db on the item
    # and run the query to delete it
    db.session.delete(inv_item)

    #Inventory.query.filter(inv_item.inv_id == inv_id).delete()

    #commit change to the db
    db.session.commit()
    inventory = user.inventory
    #send a flash confirmation message that the item was deleted
    flash(f"Item {inv_id} deleted.")
    #Take the user back to the inventory list page
    return render_template('inventory.html', user=user, inventory=inventory)

@app.route('/upd_inv_form/<int:inv_id>')
def show_inv_update(inv_id):
    inv_item = Inventory.query.get(inv_id)

    return render_template('upd_inv_form.html',inv_item=inv_item)

@app.route('/upd_inv/<int:inv_id>', methods=['POST'])
def update_inventory(inv_id):
    """Method to update an inventory item from the database"""
    user_id = session['user_id']
    user = User.query.get(user_id)

    inventory = user.inventory


    #get info from the db on the item
    inv_item = Inventory.query.get(inv_id)

    # and run the query to update it
    # NOTE TO SELF: will need to add picture path later
    inv_item.inv_name = request.form['inv_name']
    inv_item.description = request.form['description']
    inv_item.price = request.form['price']
    inv_item.count_per_package = request.form['count_per_package']
    inv_item.manufacturer = request.form['manufacturer']
    inv_item.size = request.form['size']
    inv_item.keywords = request.form['keywords']
    
    

    inv_item.save()
    

    # flash update?
    flash(f"Item {inv_id} updated.")

    # Return the user to the individual item view page to review changes
    return render_template("view_inv_item.html", inv_item=inv_item)



@app.route('/add_proj_form')
def add_proj_form():
    return render_template('proj_form.html')


@app.route('/add_project', methods=['POST'])
def add_project():
    """ Add a new project """
    user_id = session['user_id']
    name = request.form['proj_name']
    status = request.form['status']
    description = request.form['description']
    picture_path = ""
    keywords = request.form['keywords']
    tool_list = request.form['tool_list']
    supply_list = request.form['supply_list']
    directions = request.form['directions']
    URL_link = request.form['URL_link']

    app.logger.info("getting project data from form")
    new_proj = Project(user_id=user_id,
                       status=status,
                       name=name,
                       description=description,
                       picture_path=picture_path,
                       keywords=keywords,
                       tool_list=tool_list,
                       supply_list=supply_list,
                       directions=directions,
                       URL_link=URL_link)

    #add to session & commit
    # db.session.add(new_proj)
    # db.session.commit()
    new_proj.save()

    flash(f"Project: {name} added.")

    return redirect('/projects')


@app.route('/projects')
def view_projects():
    user_id = session['user_id']
    user = User.query.get(user_id)
    projects = user.projects
    
    """ Show all the projects for a particular user"""
    return render_template('projects.html',user=user, projects=projects)

@app.route('/in_progress_projects.json')
def show_ip_projects():
    user_id = session['user_id']
    user = User.query.get(user_id)
    projects = user.get_ip_projects
    print("*"*100)
    print(projects)
    return jsonify(projects)

@app.route('/view_proj_item/<int:project_id>')
def get_proj_item(project_id):
    """View an individual inv_item"""

    # get the user info saved in session
    user_id = session['user_id']

    #the inv_id was passed in with the route path
    # we can use it to query the db and get an individual inventory
    # item from the inventory table.
    proj_item = Project.query.get(project_id)
    
    #return that info to be displayed on the view_inv_item.html page

    return render_template("view_proj_item.html", proj_item=proj_item)

@app.route('/del_proj/<int:project_id>')
def delete_project(project_id):
    """Method to delete an project from the database"""
    user_id = session['user_id']
    user = User.query.get(user_id)

    proj_item = Project.query.get(project_id)
   

    #get info from the db on the item
    # and run the query to delete it
    db.session.delete(proj_item)

    #commit change to the db
    db.session.commit()

    projects = user.projects
    #send a flash confirmation message that the item was deleted
    flash(f"Item {project_id} deleted.")

    #Take the user back to the inventory list page
    return render_template('projects.html', user=user, projects=projects)


@app.route('/upd_proj_form/<int:project_id>')
def show_proj_update(project_id):
    
    #get info from the db on the item
    proj_item = Project.query.get(project_id)

    return render_template('upd_proj_form.html',proj_item=proj_item)


@app.route('/upd_proj/<int:project_id>', methods=['POST'])
def update_project(project_id):
    """Method to update an inventory item from the database"""
    user_id = session['user_id']
    user = User.query.get(user_id)

    app.logger.info(request.form)

    #get info from the db on the item
    proj_item = Project.query.get(project_id)

    # I know I should be using the request.form.get() to avoid Key Errors but 
    # something wonky is happening with the fields when I do (not getting passed
    # or saved?)

    # and run the query to update it
    # proj_item.name = request.form.get('project_name')
    # proj_item.status=request.form.get('status')
    # proj_item.description=request.form.get('description')
    # proj_item.picture_path=request.form.get('picture_path')
    # proj_item.keywords=request.form.get('keywords')
    # proj_item.tool_list=request.form.get('tool_list')
    # proj_item.supply_list=request.form.get('supply_list')
    # proj_item.directions=request.form.get('directions')
    # proj_item.URL_link=request.form.get('URL_link')

    app.logger.info(proj_item)

    proj_item.name=request.form['project_name']
    proj_item.status=request.form['status']
    proj_item.description=request.form['description']
    proj_item.picture_path=""
    proj_item.keywords=request.form['keywords']
    proj_item.tool_list=request.form['tool_list']
    proj_item.supply_list=request.form['supply_list']
    proj_item.directions=request.form['directions']
    proj_item.URL_link=request.form['URL_link']

    proj_item.save()

    # flash update?
    flash(f"Item {project_id} updated.")
    # Return the user to the individual item view page to review changes
    return render_template("view_proj_item.html", proj_item=proj_item)

@app.route('/search_form')
def search_form():
    """ display the search form"""
    return render_template('search_form.html')


@app.route('/search', methods=['POST'])
def search():
    """ Search for specific tools/supplies, and View all of the tools 
    and supplies saved in the database- for the user that is logged in """
    search_text = request.form.get('search_text')
    print("request.form.get('search_text')= ", search_text)
    user_id = session['user_id']
    user = User.query.get(user_id) 
    results = user.search_keywords(search_text)
    print(results)

    return render_template('search.html')


if __name__ == "__main__":

    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, port=5000, host="0.0.0.0")