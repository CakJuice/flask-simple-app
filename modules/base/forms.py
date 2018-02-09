import wtforms
from flask_wtf import FlaskForm

from .models import User
from validators import SameValue, UniqueValue

validators = wtforms.validators

class SignupForm(FlaskForm):
	email = wtforms.StringField("Email", validators=[
		validators.Email(),
		validators.DataRequired(),
		validators.Length(max=128),
		UniqueValue(User, 'email')
	])
	name = wtforms.StringField("Name", validators=[
		validators.DataRequired(),
		validators.Length(max=100)
	])
	password = wtforms.PasswordField("Password", validators=[
		validators.DataRequired(),
		validators.Length(min=6, max=32)
	])
	password_confirm = wtforms.PasswordField("Password Confirm", validators=[
		validators.DataRequired(),
		validators.Length(min=6, max=32),
		SameValue(same_field='password')
	])

	def save_user(self):
		user = User(password_hash=User.make_password(self.password.data))
		self.populate_obj(user)
		user.save()
		return user
