from flask import flash
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Hole:
    DB = "round_master"

    def __init__(self,data):
        self.id = data["id"]
        self.round_id  = data["round_id"]
        self.hole_number = data["hole_number"]
        self.par = data["par"]
        self.score = data["score"]

    @classmethod
    def find_by_id(cls, hole_id):
        query = "SELECT * FROM holes WHERE id = %(id)s;"
        data = {"id": hole_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all_by_round_id(cls, round_id):
        query = """SELECT * FROM holes WHERE round_id = %(round_id)s ORDER BY hole_number;"""
        data = {"round_id": round_id}
        hole_dicts = connectToMySQL(cls.DB).query_db(query, data)

        if not hole_dicts:
            return []
        
        return [cls(hole_dict) for hole_dict in hole_dicts]

    @classmethod
    def create(cls, data):
        query = """ INSERT INTO holes (round_id, hole_number, par, score, created_at, updated_at) VALUES (%(round_id)s, %(hole_number)s, %(par)s, %(score)s, NOW(), NOW());"""
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = """ UPDATE holes SET par = %(par)s, score = %(score)s, updated_at = NOW() WHERE round_id = %(round_id)s AND hole_number = %(hole_number)s;"""
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM holes WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
