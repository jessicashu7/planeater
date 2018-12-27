from main.py import db


class Class(db.Model):
    #structure of the class database

    def __repr__(self):
        return f"Classes''""



class User(db.Model):
    #structure of the User Database

    def __repr__(self):
        return f"User('')"
