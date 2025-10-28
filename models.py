from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    total_score = db.Column(db.Integer, nullable=False, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to frames
    frames = db.relationship('Frame', backref='game', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Game {self.id}: {self.total_score} on {self.date}>'

class Frame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    frame_number = db.Column(db.Integer, nullable=False)  # 1-10
    score = db.Column(db.Integer, nullable=False)
    is_strike = db.Column(db.Boolean, default=False)
    is_spare = db.Column(db.Boolean, default=False)
    is_split = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Frame {self.frame_number}: {self.score} (Game {self.game_id})>'