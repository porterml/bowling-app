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
    
    def calculate_bowling_score(self):
        """Calculate proper bowling score with strike/spare bonuses"""
        frames = sorted(self.frames, key=lambda f: f.frame_number)
        total_score = 0
        
        for i, frame in enumerate(frames):
            frame_score = 0
            
            if frame.is_strike:
                # Strike: 10 + next 2 rolls
                frame_score = 10
                
                # Add next 2 rolls
                if i < len(frames) - 1:  # Not the last frame
                    next_frame = frames[i + 1]
                    if next_frame.is_strike:
                        frame_score += 10
                        # Need second roll from next frame or frame after
                        if i + 1 < len(frames) - 1:  # Not second to last frame
                            frame_after_next = frames[i + 2]
                            frame_score += frame_after_next.roll1
                        else:  # Second to last frame, use its roll2
                            frame_score += next_frame.roll2
                    else:
                        frame_score += next_frame.roll1 + next_frame.roll2
                else:  # Last frame (10th)
                    frame_score += frame.roll2 + frame.roll3
                    
            elif frame.is_spare:
                # Spare: 10 + next roll
                frame_score = 10
                
                if i < len(frames) - 1:  # Not the last frame
                    next_frame = frames[i + 1]
                    frame_score += next_frame.roll1
                else:  # Last frame (10th)
                    frame_score += frame.roll3
                    
            else:
                # Open frame: just the pins knocked down
                frame_score = frame.roll1 + frame.roll2
            
            # Update frame score and running total
            frame.frame_score = frame_score
            total_score += frame_score
            frame.running_total = total_score
        
        self.total_score = total_score
        return total_score

class Frame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    frame_number = db.Column(db.Integer, nullable=False)  # 1-10
    roll1 = db.Column(db.Integer, nullable=False, default=0)  # First roll pins
    roll2 = db.Column(db.Integer, nullable=False, default=0)  # Second roll pins (0 if strike)
    roll3 = db.Column(db.Integer, nullable=False, default=0)  # Third roll pins (only for 10th frame)
    frame_score = db.Column(db.Integer, nullable=False, default=0)  # Calculated frame score with bonuses
    running_total = db.Column(db.Integer, nullable=False, default=0)  # Running total up to this frame
    is_strike = db.Column(db.Boolean, default=False)
    is_spare = db.Column(db.Boolean, default=False)
    is_split = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Frame {self.frame_number}: {self.roll1},{self.roll2},{self.roll3} = {self.frame_score} (Game {self.game_id})>'
    
    @property
    def total_pins(self):
        """Total pins knocked down in this frame"""
        return self.roll1 + self.roll2 + self.roll3
    
    @property
    def is_tenth_frame(self):
        """Check if this is the 10th frame"""
        return self.frame_number == 10