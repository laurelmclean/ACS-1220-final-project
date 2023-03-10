from sqlalchemy_utils import URLType
from flask_login import UserMixin
from concert_app.extensions import db

class Artist(db.Model):
    """Artist model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    hometown = db.Column(db.String(80), nullable=False)
    image = db.Column(URLType)
    genre = db.Column(db.String(80), nullable=False)
    biography = db.Column(db.String(250), nullable=False)
    upcoming_concerts = db.relationship('Concert', back_populates='artist_playing')
    fans = db.relationship(
        'User', secondary='user_artist', back_populates='favourites')

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'

class Concert(db.Model):
    """Concert model."""
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(URLType)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    venue = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date)
    artist_id = db.Column(
        db.Integer, db.ForeignKey('artist.id'), nullable=False)
    artist_playing = db.relationship('Artist', back_populates='upcoming_concerts')
    guests_attending = db.relationship(
        'User', secondary='user_concert', back_populates='attending')

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'

class User(UserMixin, db.Model):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    attending = db.relationship(
        'Concert', secondary='user_concert', back_populates='guests_attending')
    favourites = db.relationship(
        'Artist', secondary='user_artist', back_populates='fans')

    def __str__(self):
        return f'{self.username}'

    def __repr__(self):
        return f'{self.username}'

user_concert = db.Table('user_concert',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('concert_id', db.Integer, db.ForeignKey('concert.id'))
)

user_artist = db.Table('user_artist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'))
)

