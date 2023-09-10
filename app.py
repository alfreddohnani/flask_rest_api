import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow


load_dotenv()

db = SQLAlchemy()

app = Flask(__name__)

url = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = url
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

ma = Marshmallow(app)


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cards = relationship("Card", backref="cards_deck")
    shuffled = db.Column(db.Boolean, default=False)
    game_id = db.Column(db.Integer)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    players = relationship("Player", backref="game")
    deck = relationship("Deck", backref="game")


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    suit = db.Column(db.String(50), nullable=True)
    rank = db.Column(db.String(50), nullable=True)
    value = db.Column(db.Integer)
    deck_id = db.Column(db.Integer, nullable=True)
    is_drawn = db.Column(db.Boolean, default=False)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    score = db.Column(db.Integer, nullable=True)
    round_id = db.Column(db.Integer)
    game_id = db.Column(db.Integer)


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer)
    active_players = relationship("Player", backref="round_active_players")
    winners = relationship("Player", backref="round_winners")


@app.get("/")
def home():
    return "Hello world!"


@app.post("/card")
def create_card():
    suit = request.json["suit"]
    rank = request.json["rank"]
    value = request.json["value"]
    deck_id = request.json["deck_id"]
    is_drawn = request.json["is_drawn"]

    new_card = Card(suit, rank, value, deck_id, is_drawn)

    db.session.add(new_card)
    db.session.commit()

    return jsonify(new_card)


with app.app_context():
    db.create_all()
