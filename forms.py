from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, TextAreaField, DateField, FieldList, FormField, SubmitField, Form
from wtforms.validators import DataRequired, NumberRange, ValidationError
from datetime import date

class FrameForm(Form):
    """Form for individual frame data"""
    roll1 = IntegerField('Roll 1', validators=[DataRequired(), NumberRange(min=0, max=10)], default=0)
    roll2 = IntegerField('Roll 2', validators=[NumberRange(min=0, max=10)], default=0)
    roll3 = IntegerField('Roll 3', validators=[NumberRange(min=0, max=10)], default=0)
    is_strike = BooleanField('Strike')
    is_spare = BooleanField('Spare')
    is_split = BooleanField('Split')
    notes = TextAreaField('Notes', render_kw={'rows': 2, 'placeholder': 'Optional notes for this frame'})
    
    def validate_roll1(self, field):
        """Validate first roll"""
        if self.is_strike.data and field.data != 10:
            raise ValidationError('Strike frames must have 10 pins on first roll')
    
    def validate_roll2(self, field):
        """Validate second roll"""
        if self.is_strike.data and field.data != 0:
            raise ValidationError('Strike frames should have 0 pins on second roll (unless 10th frame)')
        
        if not self.is_strike.data and field.data + self.roll1.data > 10:
            raise ValidationError('Total pins cannot exceed 10 in a frame')
    
    def validate_roll3(self, field):
        """Validate third roll (only for 10th frame)"""
        if field.data > 0 and not self.is_tenth_frame:
            raise ValidationError('Third roll only allowed in 10th frame')
    
    @property
    def is_tenth_frame(self):
        """Check if this is the 10th frame - will be set by parent form"""
        return getattr(self, '_is_tenth_frame', False)
    
    def set_frame_number(self, frame_num):
        """Set frame number for validation purposes"""
        self._is_tenth_frame = (frame_num == 10)

class GameForm(FlaskForm):
    """Form for entering a complete bowling game"""
    date = DateField('Game Date', validators=[DataRequired()], default=date.today)
    game_notes = TextAreaField('Game Notes', render_kw={'rows': 3, 'placeholder': 'Optional notes about this game'})
    
    # Create 10 frame forms
    frames = FieldList(FormField(FrameForm), min_entries=10, max_entries=10)
    
    submit = SubmitField('Save Game')
    
    class Meta:
        csrf = False
    
    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        # Initialize frame labels and set frame numbers
        for i, frame in enumerate(self.frames):
            frame.set_frame_number(i + 1)
            frame.label.text = f'Frame {i + 1}'
