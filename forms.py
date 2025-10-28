from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, TextAreaField, DateField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from datetime import date

class FrameForm(FlaskForm):
    """Form for individual frame data"""
    score = IntegerField('Score', validators=[DataRequired(), NumberRange(min=0, max=30)], default=0)
    is_strike = BooleanField('Strike')
    is_spare = BooleanField('Spare')
    is_split = BooleanField('Split')
    notes = TextAreaField('Notes', render_kw={'rows': 2, 'placeholder': 'Optional notes for this frame'})
    
    def validate_score(self, field):
        """Custom validation for frame scores"""
        if self.is_strike.data and field.data != 10:
            raise ValidationError('Strike frames must have a score of 10')
        
        if self.is_spare.data and field.data < 10:
            raise ValidationError('Spare frames must have a score of at least 10')
        
        if self.is_strike.data and self.is_spare.data:
            raise ValidationError('A frame cannot be both a strike and a spare')

class GameForm(FlaskForm):
    """Form for entering a complete bowling game"""
    date = DateField('Game Date', validators=[DataRequired()], default=date.today)
    game_notes = TextAreaField('Game Notes', render_kw={'rows': 3, 'placeholder': 'Optional notes about this game'})
    
    # Create 10 frame forms
    frames = FieldList(FormField(FrameForm), min_entries=10, max_entries=10)
    
    submit = SubmitField('Save Game')
    
    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        # Initialize frame labels
        for i, frame in enumerate(self.frames):
            frame.label.text = f'Frame {i + 1}'
