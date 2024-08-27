from flask_app import app
from flask_app.models.round import Round
from flask_app.models.user import User
from flask_app.models.hole import Hole
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, render_template, redirect, request, session


@app.route("/rounds/all")
def rounds():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    rounds = Round.find_all_with_users()
    user = User.find_by_id(session["user_id"])
    return render_template("all_rounds.html", rounds=rounds, user=user)


@app.get("/rounds/new")
def new_round():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    user = User.find_by_id(session["user_id"])
    return render_template("add_round.html", user=user)


@app.post("/rounds/create_new")
def create_round():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    if not Round.form_is_valid(request.form):
        return redirect("/rounds/new")

    round_id = Round.create(request.form)

    for i in range(1, 19):
        hole_data = {
            "round_id": round_id,
            "hole_number": i,
            "par": request.form.get(f"par{i}"),
            "score": request.form.get(f"score{i}"),
        }

        Hole.create(hole_data)

    return redirect("/rounds/all")


@app.get("/rounds/<int:round_id>")
def round_details(round_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    round = Round.find_by_id_with_user(round_id)
    user = User.find_by_id(session["user_id"])

    holes = Hole.find_all_by_round_id(round_id)

    for hole in holes:
        print(f"Hole #{hole.hole_number} - Par: {hole.par}, Score: {hole.score}")

    return render_template("round_details.html", round=round, user=round.user, holes=holes)


@app.get("/rounds/<int:round_id>/edit")
def edit_round(round_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    round = Round.find_by_id(round_id)


    user = User.find_by_id(session["user_id"])

    holes = Hole.find_all_by_round_id(round_id)


    return render_template("edit_round.html", round=round, user=user, holes=holes)


@app.post("/rounds/update_round")
def update_round():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    print(request.form)

    if not Round.form_is_valid(request.form):
        return redirect(f"/rounds/{request.form['round_id']}/edit")

    Round.update(request.form)

    for i in range(1, 19):
        hole_data = {
            "round_id": request.form['round_id'],
            "hole_number": i,
            "par": request.form.get(f"par{i}"),
            "score": request.form.get(f"score{i}"),
        }

        Hole.update(hole_data)

    return redirect("/rounds/all")


@app.post("/rounds/<int:round_id>/delete")
def delete_round(round_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    print(f"Attempting to delete round with id: {round_id}")
    Round.delete(round_id)
    return redirect("/rounds/all")
