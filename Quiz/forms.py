from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError
# from Quiz.models import User


# from flask_login import UserMixin

class RegistrationForm(FlaskForm):
    username = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    contact_no = IntegerField('contact_no', validators=[DataRequired()])
    submit = SubmitField('register')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('That username is occupied. Please choose a different one.')
    #
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email is occupied. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class Add_queForm(FlaskForm):
    # id = IntegerField('id', validators=[DataRequired()])
    sub_name = StringField('sub_name', validators=[DataRequired()])
    question = StringField('question', validators=[DataRequired()])
    option1 = StringField('option1', validators=[DataRequired()])
    option2 = StringField('option2', validators=[DataRequired()])
    option3 = StringField('option3', validators=[DataRequired()])
    option4 = StringField('option4', validators=[DataRequired()])
    correct_opt = StringField('correct_opt', validators=[DataRequired()])
    submit = SubmitField('add_que')


class EditqueForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    question = StringField('question', validators=[DataRequired()])
    subject = StringField('subject', validators=[DataRequired()])
    option1 = StringField('option1', validators=[DataRequired()])
    option2 = StringField('option2', validators=[DataRequired()])
    option3 = StringField('option3', validators=[DataRequired()])
    option4 = StringField('option4', validators=[DataRequired()])
    correct_opt = StringField('correct_opt', validators=[DataRequired()])
    submit = SubmitField('update')

# class quiztakenForm(FlaskForm):
#     question = StringField('question', validators=[DataRequired()])
#     selected_option = StringField('options', validators=[DataRequired()])
#     submit = SubmitField('quiz_taken')
