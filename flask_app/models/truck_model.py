from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model
import re

class Truck:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.date = data['date']
        self.cuisine = data['cuisine']
        self.price = data['price']
        self.rating = data['rating']
        self.website = data['website']
        self.comments = data['comments']
        self.image_url = data['image_url']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    # method for creating new truck entry
    @classmethod
    def create(cls,data):
        query = """
        INSERT INTO trucks (name,date,cuisine,price,rating,website,comments,user_id)
        VALUES (%(name)s,%(date)s,%(cuisine)s,%(price)s,%(rating)s,%(website)s,%(comments)s,%(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    # method for getting all trucks
    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM trucks JOIN users ON trucks.user_id = users.id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_trucks = []
        if results:
            for row in results:
                this_truck = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                this_user = user_model.User(user_data)
                this_truck.visitor = this_user
                all_trucks.append(this_truck)
        return all_trucks

    # method for getting one truck w/ newly created attribute of "visitor" through a join
    @classmethod
    def get_one(cls,data):
        query = """
        SELECT * FROM trucks JOIN users ON trucks.user_id = users.id
        WHERE trucks.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            row = results[0]
            this_truck = cls(row)
            user_data = {
                **row,
                'id': row['users.id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            this_user = user_model.User(user_data)
            this_truck.visitor = this_user
            return this_truck
        return False

    # method for updating/editing truck entry
    @classmethod
    def update(cls,data):
        query = """
        UPDATE trucks SET name = %(name)s, date = %(date)s,
        cuisine = %(cuisine)s, price = %(price)s, 
        rating = %(rating)s, website = %(website)s,
        comments = %(comments)s
        WHERE trucks.id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    # method for deleting single truck entry
    @classmethod
    def delete(cls,data):
        query = """
        DELETE FROM trucks WHERE id = %(id)s
        """
        return connectToMySQL(DATABASE).query_db(query,data)


    # validation method for new truck entry
    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data["name"]) < 3:
            flash("name must be at least 3 characters")
            is_valid = False
        if "rating" not in form_data:
            flash("rating required")
            is_valid = False
        if "price" not in form_data:
            flash("price required")
            is_valid = False
        if len(form_data["comments"]) < 3:
            flash("comments required")
            is_valid = False
        return is_valid
        


