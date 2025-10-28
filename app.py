from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_migrate import Migrate
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bowling.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import models and initialize db
from models import db, Game, Frame
from forms import GameForm

# Initialize db with app
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    """Analytics dashboard - main page"""
    games = Game.query.order_by(Game.date.desc()).all()
    
    if not games:
        return render_template('index.html', 
                             total_games=0, 
                             avg_score=0, 
                             high_score=0, 
                             low_score=0,
                             frame_averages=[],
                             recent_games=[],
                             stats={})
    
    # Calculate basic statistics
    total_games = len(games)
    scores = [game.total_score for game in games]
    avg_score = sum(scores) / len(scores) if scores else 0
    high_score = max(scores) if scores else 0
    low_score = min(scores) if scores else 0
    
    # Calculate frame averages
    frame_averages = []
    for frame_num in range(1, 11):
        frame_scores = []
        for game in games:
            frame = Frame.query.filter_by(game_id=game.id, frame_number=frame_num).first()
            if frame:
                frame_scores.append(frame.score)
        
        if frame_scores:
            avg = sum(frame_scores) / len(frame_scores)
            frame_averages.append({'frame': frame_num, 'average': round(avg, 1)})
        else:
            frame_averages.append({'frame': frame_num, 'average': 0})
    
    # Calculate strike/spare/split statistics
    all_frames = Frame.query.join(Game).all()
    total_frames = len(all_frames)
    
    strikes = len([f for f in all_frames if f.is_strike])
    spares = len([f for f in all_frames if f.is_spare])
    splits = len([f for f in all_frames if f.is_split])
    
    stats = {
        'strikes': {'count': strikes, 'percentage': round((strikes/total_frames)*100, 1) if total_frames > 0 else 0},
        'spares': {'count': spares, 'percentage': round((spares/total_frames)*100, 1) if total_frames > 0 else 0},
        'splits': {'count': splits, 'percentage': round((splits/total_frames)*100, 1) if total_frames > 0 else 0}
    }
    
    # Recent games (last 10)
    recent_games = games[:10]
    
    return render_template('index.html',
                         total_games=total_games,
                         avg_score=round(avg_score, 1),
                         high_score=high_score,
                         low_score=low_score,
                         frame_averages=frame_averages,
                         recent_games=recent_games,
                         stats=stats)

@app.route('/add-game', methods=['GET', 'POST'])
def add_game():
    """Add a new bowling game"""
    form = GameForm()
    
    if form.validate_on_submit():
        # Create new game
        game = Game(
            date=form.date.data,
            notes=form.game_notes.data
        )
        db.session.add(game)
        db.session.flush()  # Get the game ID
        
        # Calculate total score
        total_score = 0
        
        # Add frames
        for i, frame_form in enumerate(form.frames):
            frame = Frame(
                game_id=game.id,
                frame_number=i + 1,
                score=frame_form.score.data,
                is_strike=frame_form.is_strike.data,
                is_spare=frame_form.is_spare.data,
                is_split=frame_form.is_split.data,
                notes=frame_form.notes.data
            )
            db.session.add(frame)
            total_score += frame_form.score.data
        
        # Update game with total score
        game.total_score = total_score
        db.session.commit()
        
        flash('Game added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_game.html', form=form)

@app.route('/games')
def games():
    """List all games"""
    games = Game.query.order_by(Game.date.desc()).all()
    return render_template('games.html', games=games)

@app.route('/game/<int:game_id>')
def game_detail(game_id):
    """View individual game details"""
    game = Game.query.get_or_404(game_id)
    frames = Frame.query.filter_by(game_id=game_id).order_by(Frame.frame_number).all()
    return render_template('game_detail.html', game=game, frames=frames)

@app.route('/delete-game/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    """Delete a game"""
    game = Game.query.get_or_404(game_id)
    
    # Delete associated frames first
    Frame.query.filter_by(game_id=game_id).delete()
    
    # Delete the game
    db.session.delete(game)
    db.session.commit()
    
    flash('Game deleted successfully!', 'success')
    return redirect(url_for('games'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)
