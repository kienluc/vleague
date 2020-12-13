
from app import app, login, utils
from flask import render_template, request, redirect
from app.models import *
from flask_login import login_user


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/schedule")
def schedule():
    matches = Match.query.all()
    return render_template("schedule.html", matches=matches, results=utils.read_result())


@app.route("/ranking")
def ranking():
    return render_template("ranking.html")


@app.route("/teams")
def team_list():
    kw = request.args.get("keyword")
    return render_template("teams.html", teams=utils.read_teams(kw))


@app.route("/reportgoals")
def goal_list():
    return render_template("reportgoals.html", players=utils.read_goals(), teams=Team.query.all())


@app.route("/players")
def player_list():
    return render_template("players.html")


@app.route("/login-admin", methods=["post", "get"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        user = User.query.filter(User.username == username.strip(),
                                 User.password == password.strip()).first()

        if user:
            login_user(user=user)

    return redirect("/admin")


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)