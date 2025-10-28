# Bowling Analytics App

A Flask-based web application for tracking bowling performance with detailed analytics and frame-by-frame scoring.

## Features

- **Frame-by-Frame Scoring**: Enter scores for each of the 10 frames with strike, spare, and split tracking
- **Analytics Dashboard**: View comprehensive statistics including:
  - Average score by frame (identify weak frames)
  - Strike, spare, and split percentages
  - Total games, average score, highest/lowest scores
  - Recent games overview
- **Game Management**: Add, view, and delete bowling games
- **Responsive Design**: Works on desktop and mobile devices
- **Visual Charts**: Interactive charts showing frame performance and score progression

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML templates with Jinja2, Bootstrap 5, Chart.js
- **Forms**: Flask-WTF with validation
- **Styling**: Custom CSS with responsive design

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd bowling-app
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to `http://localhost:5000`

## Usage

### Adding a Game

1. Click "Add Game" in the navigation
2. Select the game date
3. Enter scores for each frame (1-10)
4. Mark frames as strikes, spares, or splits using checkboxes
5. Add optional notes for frames or the entire game
6. Click "Save Game"

### Viewing Analytics

- **Dashboard**: Main page shows overall statistics and recent games
- **All Games**: View a list of all games with summary statistics
- **Game Details**: Click on any game to see frame-by-frame breakdown

### Frame Scoring Rules

- **Strike**: Mark checkbox and enter score of 10
- **Spare**: Mark checkbox and enter score of 10-29 (depending on next rolls)
- **Split**: Mark checkbox for difficult spare situations
- **Regular**: Enter score 0-9 for open frames

## Project Structure

```
bowling-app/
├── app.py                 # Main Flask application
├── models.py             # Database models (Game, Frame)
├── forms.py              # WTForms for score entry
├── requirements.txt      # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css    # Custom styles
│   └── js/
│       └── main.js      # JavaScript functionality
├── templates/
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Analytics dashboard
│   ├── add_game.html    # Game entry form
│   ├── games.html       # List of past games
│   └── game_detail.html # Individual game view
├── bowling.db           # SQLite database (created automatically)
├── vercel.json          # Vercel deployment config
└── Procfile             # Heroku deployment config
```

## Deployment

### Option 1: Railway (Recommended)

1. Push your code to GitHub
2. Connect your GitHub repo to Railway
3. Railway will automatically detect Flask and deploy
4. Add environment variables if needed

### Option 2: Render

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

### Option 3: Heroku

1. Install Heroku CLI
2. Create a Heroku app: `heroku create your-app-name`
3. Deploy: `git push heroku main`

**Note**: For production deployment, consider using PostgreSQL instead of SQLite for better performance and reliability.

## Development

### Database Migrations

If you need to modify the database schema:

```bash
flask db init
flask db migrate -m "Description of changes"
flask db upgrade
```

### Adding New Features

- **Models**: Add new database models in `models.py`
- **Routes**: Add new routes in `app.py`
- **Templates**: Create new HTML templates in `templates/`
- **Forms**: Add new forms in `forms.py`

## Future Enhancements

- **User Authentication**: Multi-user support with login/registration
- **Advanced Analytics**: More detailed statistics and trends
- **League Support**: Track multiple leagues or tournaments
- **Export Data**: Export game data to CSV/Excel
- **Mobile App**: React Native or Flutter mobile app
- **Social Features**: Share achievements and compete with friends

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m "Add feature"`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is open source and available under the MIT License.
