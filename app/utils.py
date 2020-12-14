from app.models import *
from operator import attrgetter #sort-mutilple-condition


def read_teams(keyword=None):
    teams = Team.query.all()
    if keyword:
        teams = [t for t in teams if t.name.lower().find(keyword.lower()) >= 0]

    return teams


def read_players(selected, keyword=None):
    players = Player.query.all()
    if keyword:
        if selected == "playername":
            players = [p for p in players if p.name.lower().find(keyword.lower()) >= 0]
        try:
            if selected =="numofgoals":
                players = [p for p in players if p.total_goals == int(keyword)]
        except:
            players=[]
    else:
        players = players
    return players


def read_goals():
    goals = Goal.query.all()
    players = Player.query.all()
    for player in players:
        for goal in goals:
            if player.id == goal.player_id:
                player.total_goals += 1
    players.sort(key=attrgetter("total_goals"), reverse=True)

    return players


def read_result():
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


def read_ranking():
    matches = Match.query.all()
    goals = Goal.query.all()
    players = Player.query.all()
    teams = Team.query.all()
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
    #Cộng dồn điểm vào score của home và away