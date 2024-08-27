from flask import flash
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User


class Round:
    DB = "round_master"

    def __init__(self, form_data):
        self.id = form_data["id"]
        self.coursename = form_data["coursename"]
        self.date_played = form_data["date_played"]
        self.out_score = form_data["out_score"]
        self.in_score = form_data["in_score"]
        self.total_score = form_data["total_score"]
        self.created_at = form_data["created_at"]
        self.updated_at = form_data["updated_at"]
        self.user = None

    @staticmethod
    def form_is_valid(form_data):

        is_valid = True

        if len(form_data["date_played"]) == 0:
            flash("Please enter valid date played.")
            is_valid = False
        else:
            try:
                datetime.strptime(form_data["date_played"], "%Y-%m-%d")
            except:
                flash("Invalid date played.")
                is_valid = False

        if len(form_data["coursename"]) == 0:
            flash("Course name is required.")
            is_valid = False

        for i in range(1, 19):
            par = form_data.get(f"par{i}")
            score = form_data.get(f"score{i}")

            if par is None or par == "":
                flash(f"Par for hole {i} is required.")
                is_valid = False

            if score is None or score == "":
                flash(f"Score for hole {i} is required.")
                is_valid = False

        return is_valid

    @classmethod
    def find_all(cls):
        query = """SELECT * FROM rounds"""
        list_of_dicts = connectToMySQL(Round.DB).query_db(query)

        rounds = []
        for each_dict in list_of_dicts:
            round = Round(each_dict)
            rounds.append(round)
        return rounds

    @classmethod
    def find_all_with_users(cls):
        query = """SELECT * FROM rounds JOIN users ON rounds.user_id = users.id"""

        list_of_dicts = connectToMySQL(Round.DB).query_db(query)

        rounds = []
        for each_dict in list_of_dicts:
            round = Round(each_dict)
            user_data = {
                "id": each_dict["users.id"],
                "firstname": each_dict["firstname"],
                "lastname": each_dict["lastname"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["users.created_at"],
                "updated_at": each_dict["users.updated_at"],
            }
            user = User(user_data)
            round.user = user
            rounds.append(round)
        return rounds

    @classmethod
    def find_by_id(cls, round_id):
        query = """SELECT * FROM rounds WHERE id = %(round_id)s"""
        data = {"round_id": round_id}
        list_of_dicts = connectToMySQL(Round.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None

        round = Round(list_of_dicts[0])
        return round

    @classmethod
    def find_by_id_with_user(cls, round_id):
        query = """SELECT * FROM rounds JOIN users ON rounds.user_id = users.id WHERE rounds.id = %(round_id)s"""

        data = {"round_id": round_id}
        list_of_dicts = connectToMySQL(Round.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None

        each_dict = list_of_dicts[0]
        round = Round(each_dict)
        user_data = {
            "id": each_dict["users.id"],
            "firstname": each_dict["firstname"],
            "lastname": each_dict["lastname"],
            "email": each_dict["email"],
            "password": each_dict["password"],
            "created_at": each_dict["users.created_at"],
            "updated_at": each_dict["users.updated_at"],
        }
        round.user = User(user_data)
        return round

    @classmethod
    def create(cls, form_data):
        out_score = form_data.get("out_score")
        if out_score is None or out_score == "":
            raise ValueError("out_score is required")
        
        data = {
            "coursename": form_data["coursename"],
            "date_played": form_data["date_played"],
            "out_score": int(form_data["out_score"]),
            "in_score": int(form_data["in_score"]),
            "total_score": int(form_data["total_score"]),
            "user_id": int(form_data["user_id"]),
        }

        query = """INSERT INTO rounds (coursename, date_played, user_id, out_score, in_score, total_score, created_at, updated_at) 
        VALUES (%(coursename)s, %(date_played)s, %(user_id)s, %(out_score)s, %(in_score)s, %(total_score)s, NOW(), NOW())"""

        round_id = connectToMySQL(Round.DB).query_db(query, data)
        return round_id


    @classmethod
    def update(cls, form_data):
        query = """UPDATE rounds SET coursename = %(coursename)s, date_played = %(date_played)s, out_score = %(out_score)s, in_score = %(in_score)s, total_score = %(total_score)s, updated_at = NOW() WHERE id = %(round_id)s"""
        connectToMySQL(Round.DB).query_db(query, form_data)
        return

    @classmethod
    def delete(cls, round_id):
        query = "DELETE FROM rounds WHERE id = %(round_id)s"
        data = {"round_id": round_id}
        connectToMySQL(Round.DB).query_db(query, data)
        return
