from app.models import *
from operator import attrgetter #sort-mutilple-condition


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
    players.sort(key=attrgetter("total_goals"), reverse=True)
    return players


def read_result():
    matches = Match.query.all()
    goals = Goal.query.all()
    players = Player.query.all()
    teams = Team.query.all()
    for team in teams:
        team.win_goals = 0
        team.lose_goals = 0
    for match in matches:
        for player in players:
            for goal in goals:
                if match.id == goal.match_id and goal.player_id == player.id:
                    if player.team_id == match.home_id:
                        for team in teams:
                            if team.id == match.home_id:
                                team.win_goals += 1
                            elif team.id == match.away_id:
                                team.lose_goals += 1
                    elif player.team_id == match.away_id:
                        for team in teams:
                            if team.id == match.away_id:
                                team.win_goals += 1
                            elif team.id == match.home_id:
                                team.lose_goals += 1
    home_goals = 0
    away_goals = 0
    for match in matches:
        for player in players:
            for goal in goals:
                if goal.player_id == player.id and match.home_id == player.team_id:
                    home_goals += 1
                if goal.player_id == player.id and match.away_id == player.team_id:
                    away_goals += 1
        if home_goals > away_goals:
            match.home.win += 1
            match.away.lose += 1

        if home_goals == away_goals:
            match.home.tie += 1
            match.away.tie += 1

        if home_goals < away_goals:
            match.home.lose += 1
            match.away.win += 1

        match.home.score = match.home.win*3 + match.home.tie
        match.away.score = match.away.win*3 + match.away.tie

    teams.sort(key=attrgetter("score"), reverse=True)
    return teams


db.session.commit()




