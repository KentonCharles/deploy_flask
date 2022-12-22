from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # method for creating new user
    @classmethod
    def create(cls,data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    # method for getting a single user by id
    @classmethod
    def get_by_id(cls,data):
        query = """
        SELECT * FROM users WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False

    # method for getting single user by email
    @classmethod
    def get_by_email(cls,data):
        query = """
        SELECT * FROM users WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False

    # validation method for new user registration form
    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash('name must be at least 2 characters', 'reg')
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash('name must be at least 2 characters', 'reg')
            is_valid = False
        if len(form_data['email']) < 1:
            flash('email required', 'reg')
            is_valid = False
        elif not EMAIL_REGEX.match(form_data['email']):
            flash('invalid email', 'reg')
            is_valid = False
        else:
            data = {
                "email": form_data['email']
            }
            potential_user = User.get_by_email(data)
            if potential_user:
                flash('email aleady exists', 'reg')
                is_valid = False
        if len(form_data['password']) < 8:
            flash('password must be at least 8 characters', 'reg')
            is_valid = False
        elif not form_data['password'] == form_data['conf_password']:
            flash('passwords must match', 'reg')
        return is_valid
        
