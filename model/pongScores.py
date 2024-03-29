""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import datetime
import os, base64
import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError


class Pong(db.Model):
    __tablename__ = 'pongs'  

    # Define the Pong schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _user1 = db.Column(db.String(255), unique=False, nullable=False)
    _user2 = db.Column(db.String(255), unique=False, nullable=False)
    _score1 = db.Column(db.String(255), unique=False, nullable=False)
    _score2 = db.Column(db.String(255), unique=False, nullable=False)
    _result1 = db.Column(db.String(255), unique=False, nullable=False)
    _result2 = db.Column(db.String(255), unique=False, nullable=False)
    _gameDatetime = db.Column(db.DateTime)

    # constructor of a Pong object, initializes the instance variables within object (self)
    def __init__(self, user1="none", user2="none", score1='0', score2='0', result1="none", result2="none", gameDatetime=datetime): # variables with self prefix become part of the object, 
        self._user1 = user1
        self._user2 = user2
        self._score1 = score1
        self._score2 = score2
        self._result1 = result1
        self._result2 = result2
        self._gameDatetime = gameDatetime
    
    # a getter method, extracts email from object
    @property
    def user1(self):
        return self._user1
    
    # a setter function, allows user1 to be updated after initial object creation. This one for player 1
    @user1.setter
    def user1(self, user1):
        self._user1 = user1
        
    @property
    def user2(self):
        return self._user2
    
    # a setter function for player 2
    @user2.setter
    def user2(self, user2):
        self._user2 = user2
    
    @property
    def score1(self):
        return self._score1
    
    # a setter function for score for player 1
    @score1.setter
    def score1(self, score1):
        self._score1 = score1
    
    @property
    def score2(self):
        return self._score2
    
    # a setter function for score for player 2
    @score2.setter
    def score2(self, score2):
        self._score2 = score2

    @property
    def result1(self):
        return self._result1
    
    # a setter function for the result of player 1
    @result1.setter
    def result1(self, result1):
        self._result1 = result1

    @property
    def result2(self):
        return self._result2
    
    # a setter function for the result of player 1
    @result2.setter
    def result2(self, result2):
        self._result2 = result2
    
    # gameDatetime property is returned as string
    @property
    def gameDatetime(self):
        gameDatetime_string = self._gameDatetime.strftime('%m-%d-%Y %H:%M:%S')
        return gameDatetime_string
    
    # gameDatetime should be have verification for type date
    @gameDatetime.setter
    def gameDatetime(self, gameDatetime):
        self._gameDatetime = gameDatetime
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.make_dict())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from Pong(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Pongs table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
    
    # CRUD update: updates user1, user2, score1, score2, result1, result2
    # returns self
    def update(self, user1="", user2="", score1="", score2="", result1="", result2=""):
        """only updates values with length"""
        if len(user1) == 3:
            self.user1 = user1
        if len(user2) == 3:
            self.user2 = user2
        """only updates values with scores greater than 0"""
        if int(score1) >= 0:
            self.score1 = score1
        if int(score2) >= 0:
            self.score2 = score2
        """only updates when the results are either won or loss"""
        if result1 in ("Win", "Loss"):
            self.result1 = result1
        if result2 in ("Win", "Loss"):
            self.result2 = result2
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def make_dict(self):
        return {
            "id": self.id,
            "user1": self.user1,
            "user2": self.user2,
            "score1": self.score1,
            "score2": self.score2,
            "result1": self.result1,
            "result2": self.result2,
            "gameDatetime": self.gameDatetime
        }



"""Database Creation and Testing """


# Builds working data for testing
def initPong():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        game1 = Pong('AAA', 'BBB', '1', '5', 'Loss', 'Win', datetime(2023, 1, 22, 15, 30, 0))
        game2 = Pong('AAB', 'ABC', '2', '5', 'Loss', 'Win', datetime(2023, 1, 21, 14, 15, 0))
        game3 = Pong('AAC', 'GHI', '5', '4', 'Win', 'Loss', datetime(2023, 1, 20, 13, 0, 0))
        game4 = Pong('AAD', 'FGH', '5', '1', 'Win', 'Loss', datetime(2023, 1, 19, 12, 45, 0))
        game5 = Pong('AAE', 'TYU', '3', '5', 'Loss', 'Win', datetime(2023, 1, 22, 11, 30, 0))

        games = [game1, game2, game3, game4, game5]

        """Builds sample game data"""
        for game in games:
            try:
                game.create()
            except IntegrityError:
                '''fails with bad data'''
                db.session.remove()
                print(f"Error in {game.user1} and/or {game.user2}")
        
