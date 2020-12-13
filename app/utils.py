from app.models import *
from sqlalchemy.sql.functions import func


def read_teams(keyword=None):
    teams = Team.query.all()
    if keyword:
        teams = [t for t in teams if t.name.lower().find(keyword.lower()) >= 0]

    return teams


def read_goals():
    goals = Goal.query.all()
    players = Player.query.all()
    for player in players:
        for goal in goals:
            if player.id == goal.player_id:
                player.total_goals += 1
    players.sort(key=lambda x: x.total_goals, reverse=True)
    return players


def read_result():
    teams = Team.query.all()
    matches = Match.query.all()
    goals = Goal.query.all()
    players = Player.query.all()
    home_goals = 0
    away_goals = 0
    for match in matches:
        for goal in goals:
            for player in players:
                if match.id == goal.match_id and goal.player_id == player.id:
                    if player.team_id == match.home_id:
                        home_goals += 1
                    elif player.team_id == match.away_id:
                        away_goals += 1

    return str(home_goals) + " - " + str(away_goals)
