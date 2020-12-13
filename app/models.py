
from app import db, admin
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME, Boolean, Enum as EnumData, DateTime, Date
from sqlalchemy.orm import relationship, backref
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user, logout_user
from flask_admin import BaseView, expose
from flask import redirect
from enum import Enum


class GoalType(Enum):
    A = 1
    B = 2
    C = 3


class ResultType(Enum):
    win = 3
    lose = 0
    tie = 1


class PlayerType(Enum):
    local = "Cầu thủ quốc nội"
    foreign = "Cầu thủ nước ngoài"


class Position(Enum):
    HLV = "Huấn luyện viên"
    GK = "Thủ môn"
    LF = "Tiền đạo cánh trái"
    RF = "Tiền đạo cánh phải"
    CF = "Tiền đạo trung tâm"
    SW = "Trung vệ thòng"
    ST = "Tiền đạo cắm - Trung Phong"
    CB = "Trung vệ"
    LB = "Hậu vệ trái"
    RB = "Hậu vệ phải"
    RS = "Hậu vệ phải"
    LS = "Hậu vệ trái"
    LM = "Tiền vệ trái"
    RM = "Tiền vệ phải"


class Priority(Enum):
    Diem = 1
    HieuSo = 2
    SoBanThang = 3
    DoiKhang = 4


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


season_team = db.Table("season_team",
                       Column("season_id", Integer, ForeignKey("season.id"), primary_key=True),
                       Column("team_id", Integer, ForeignKey("team.id"), primary_key=True))


class Season(db.Model):
    __tablename__ = "season"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    number_of_team = Column(Integer, nullable=False)
    teams = relationship("Team", secondary="season_team", lazy="subquery", backref=backref("seasons", lazy=True))
    rule_id = Column(Integer, ForeignKey("rule.id"))
    rule = relationship("Rule", backref=backref("season", uselist=False))
    rounds = relationship("Round", backref="season", lazy=True)

    def __str__(self):
        return self.name


class Rule(db.Model):
    __tablename__ = "rule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    min_age = Column(Integer, nullable=False, default=16)
    max_age = Column(Integer, nullable=False, default=40)
    min_total_player = Column(Integer, nullable=False, default=15)
    max_total_player = Column(Integer, nullable=False, default=22)
    max_total_foreigner = Column(Integer, nullable=False, default=3)
    max_time_score = Column(Integer, nullable=False, default=96)
    win_score = Column(Integer, nullable=False, default=3)
    tie_score = Column(Integer, nullable=False, default=1)
    lose_score = Column(Integer, nullable=False, default=0)
    priority = Column(EnumData(Priority), nullable=False)

    def __str__(self):
        return "General" + " " + str(self.__tablename__)


class Round(db.Model):
    __tablename__ = "round"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    season_id = Column(Integer, ForeignKey("season.id"), nullable=False)
    matches = relationship("Match", backref="round", lazy=True)

    def __str__(self):
        return self.name


class Team(db.Model):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    stadium = Column(String(50), nullable=False)
    players = relationship('Player', backref='team', lazy=True)
    score = Column(Integer, nullable=True, default=0)

    def __str__(self):
        return self.name


match_player = db.Table("match_player",
                        Column("match_id", Integer, ForeignKey("match.id"), primary_key=True),
                        Column("player_id", Integer, ForeignKey("player.id"), primary_key=True)
                        )


class Match(db.Model):

    __tablename__ = "match"
    id = Column(Integer, primary_key=True, autoincrement=True)
    home_id = Column(Integer, ForeignKey("team.id"), nullable=False)
    away_id = Column(Integer, ForeignKey("team.id"), nullable=False)
    home = relationship("Team", foreign_keys=[home_id])
    away = relationship("Team", foreign_keys=[away_id])
    MatchTime = Column(DATETIME, nullable=False)
    stadium = Column(String(50), nullable=False)
    goal = relationship("Goal", backref="match", lazy=True)
    round_id = Column(Integer, ForeignKey("round.id"), nullable=False)

    def __str__(self):
        return self.home.name + " - " + self.away.name


class Player(db.Model):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=False)
    position = Column(EnumData(Position), nullable=False, default="")
    player_type = Column(EnumData(PlayerType), nullable=False, default="")
    total_goals = Column(Integer, nullable=True, default=0)
    team_id = Column(Integer, ForeignKey(Team.id), nullable=False)
    goals = relationship("Goal", backref="player", lazy=True)
    matches = relationship("Match", secondary="match_player", lazy="subquery", backref=backref("players", lazy=True))

    def __str__(self):
        return self.name


class Goal(db.Model):
    __tablename__ = "goal"
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    goal_type = Column(EnumData(GoalType), nullable=False)
    thoi_diem = Column(DATETIME, nullable=False)
    match_id = Column(Integer, ForeignKey("match.id"), nullable=False)

    def __str__(self):
        return str(self.goal_type.name) + " - " + str(self.thoi_diem)


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


class RuleView(ModelView):
    column_display_pk = False
    can_edit = True
    can_create = True
    can_delete = False

    def is_accessible(self):
        return current_user.is_authenticated


class GeneralView(ModelView):
    column_display_pk = False
    can_create = True
    can_edit = True
    can_delete = True

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(GeneralView(Season, db.session))
admin.add_view(GeneralView(Round, db.session))
admin.add_view(GeneralView(Team, db.session))
admin.add_view(GeneralView(Player, db.session))
admin.add_view(GeneralView(Match, db.session))
admin.add_view(GeneralView(Goal, db.session))
admin.add_view(RuleView(Rule, db.session))
admin.add_view(LogoutView(name="Logout"))

if __name__ == "__main__":
    db.drop_all()
    db.create_all()


