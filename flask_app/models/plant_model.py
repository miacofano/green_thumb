from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model

db = 'green_thumb_database'

class Plant:
    def __init__ (self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.water = db_data['water']
        self.light = db_data['light']
        self.food = db_data['food']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.owner = None


    @staticmethod
    def validate_plant(plant):
        is_valid = True
        if len(plant['name']) <= 0:
            flash("The plant name can not be blank.")
            is_valid = False
        if len(plant['water']) <= 0:
            flash("The frequency in which the plant needs water can not be blank.")
            is_valid = False
        if len(plant['light']) <= 0:
            flash("The amount of light the plant needs can not be blank.")
            is_valid = False
        if len(plant['food']) <= 0:
            flash("The frequency in which the plant needs food can not be blank.")
            is_valid = False
        return is_valid


    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO plants (name, water, light, food, user_id, created_at, updated_at) 
        VALUES (%(name)s, %(water)s, %(light)s, %(food)s, %(user_id)s, NOW(),NOW());
        """
        result = connectToMySQL(db).query_db(query, data)
        return result
    
    @classmethod
    def delete(cls,data):
        query = """
                DELETE FROM plants
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_plants_with_user(cls):
        query = "SELECT * FROM plants JOIN users ON plants.user_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        all_plants = []
        for x in results:
            one_plant = cls(x)
            plant_with_user_info = {
                'id': x['users.id'],
                'first_name': x['first_name'],
                'last_name': x['last_name'],
                'email': x['email'],
                'password': x['password'],
                'created_at': x['created_at'],
                'updated_at': x['updated_at']
            }
            user = user_model.User(plant_with_user_info)
            one_plant.owner = user
            all_plants.append(one_plant)
            print(all_plants)
        return all_plants
