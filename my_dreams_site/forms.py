
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PurchaseForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])

    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Purchase')

class GoalForm(FlaskForm):
    target_amount = FloatField('Target Amount', validators=[DataRequired()])
    submit = SubmitField('Set Goal')

class ContributionForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Contribution')
