
"""Models and database functions for MMH Hackbright project."""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


##############################################################################
# Model definitions

class ModelMixin:
    def save(self):
        db.session.add(self)
        db.session.commit()


class User(ModelMixin, db.Model):
    """User of MHH website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String, nullable=False)
    fname = db.Column(db.String(50), nullable = False)
    lname = db.Column(db.String(50), nullable = False)

    
    projects = db.relationship("Project", backref=db.backref("projects",
                               order_by=user_id))
    inventory = db.relationship("Inventory", backref=db.backref("inventory",
                                order_by=user_id))

    def __repr__(self):
        return f"""<User user_id={self.user_id}
                   username={self.username}
                   email={self.email}
                   password={self.password}
                   fname={self.name}
                   lname={self.name}>"""

    # def create_user():
    #     """ Method to take kwargs and create a user """
    #     user = User()
    #     return user

    def create_hashedpw(self, password):
        self.password = generate_password_hash(password)

    def login(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
            "user_id": self.user_id, "username": self.username,
            "email": self.email, "password": self.password,
            "fname": self.fname, "lname": self.lname
        }
    def get_ip_projects(self):
        """Function to return the projects for a user that are in progress
           ie. their status='i'
        """
        projects = Project.query.filter(Project.user_id == self.user_id)
        ip_projects = projects.filter(Project.status == "i").all()
        return ip_projects

    def search_keywords(self, search_parms):
        """Function to search the user's iventory for a match on the 
        search parameters in the keywords column"""
        #get the rows in inventory that match based on the current user_id
        user_inv = Inventory.query.filter(Inventory.user_id == self.user_id)
        # filter out - get the inv item rows that match the search parms
        matches = user_inv.filter(Inventory.keywords.like(f"%{search_parms}%")).all()
        return matches
    



class Inventory(ModelMixin, db.Model):
    """Table containing each item in inventory (whether tool or supply)"""
    __tablename__ = "inventory"

    inv_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey("users.user_id"))
    inv_name = db.Column(db.String(100), nullable=False)
    inv_type = db.Column(db.String(1), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.Float(), nullable=True)
    count_per_package = db.Column(db.Integer, nullable=True)
    manufacturer = db.Column(db.String(40), nullable=True)
    size = db.Column(db.String(25), nullable = True)
    picture_path = db.Column(db.String(200), nullable=True)
    keywords = db.Column(db.String(500), nullable=True)

    # user = db.relationship("User",
    #                        backref=db.backref("users",
    #                                           order_by=user_id))
    

    def __repr__(self):
        return f"""<Inv inv_id={self.user_id}
                    user_id={self.user_id}
                    inv_name={self.inv_name}
                    inv_type={self.inv_type}
                    description={self.description}
                    price={self.price}
                    count_per_package={self.count_per_package}
                    manufacturer={self.manufacturer}
                    size={self.size}
                    picture_path={self.picture_path}
                    keywords={self.keywords}
                    >"""
    def serialize(self):
        return {
            "inv_id": self.inv_id,
            "user_id": self.user_id,
            "inv_name":self.name,
            "inv_type": self.inv_type,
            "description": self.description,
            "price": self.price,
            "count_per_package": self.count_per_package,
            "manufacturer": self.manufacturer,
            "size": self.size,
            "picture_path": self.picture_path,
            "keywords": self.keywords
            
        }


class Project(ModelMixin, db.Model):
    """ Table containing all the projects belonging to each user
    """
    __tablename__ = "projects"

    project_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    status = db.Column(db.String(1), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    
    # Store the Path to the picture
    picture_path = db.Column(db.String(100), nullable=True)
    keywords = db.Column(db.String(500), nullable=True)

    tool_list = db.Column(db.String(500), nullable=True)
    supply_list = db.Column(db.String(500), nullable=True)
    directions = db.Column(db.String(1500), nullable=True)
    URL_link = db.Column(db.String(300), nullable=True)
    

    def __repr__(self):
        return f"""<Project project_id={self.project_id}
                   user_id={self.user_id}
                   status={self.status}
                   name={self.name}
                   description={self.description}
                   picture_path={self.picture_path}
                   keywords={self.keywords}
                   tool_list={self.tool_list}
                   supply_list={self.supply_list}
                   directions={self.directions}
                   URL_link={self.URL_link}>"""

    def serialize(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "fname": self.fname,
            "lname": self.lname,
            "user_id":self.user_id,
            "status":self.status,
            "name":self.name,
            "description": self.description,
            "picture_path": self.picture_path,
            "keywords": self.keywords,
            "tool_list": self.tool_list,
            "supply_list": self.supply_list,
            "directions": self.directions,
            "URL_link": self.URL_link
        }


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ManageMyHoard'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")

