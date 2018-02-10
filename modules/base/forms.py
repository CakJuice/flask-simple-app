# -*- coding: utf-8 -*-

"""Forms in base modules

Author:
	@CakJuice <hd.brandoz@gmail.com>
"""

import wtforms
from flask_wtf import FlaskForm

from validators import SameValue, UniqueValue
from .models import User

validators = wtforms.validators

class SignupForm(FlaskForm):
	"""To handle Signup user form
	"""

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
		"""To save user when signup is valid

		Returns:
			Recordset -- Result of create user
		"""

		user = User(password_hash=User.make_password(self.password.data))
		self.populate_obj(user)
		user.save()
		return user

class LoginForm(FlaskForm):
	"""To handle Signup user form
	"""

	email = wtforms.StringField("Email", validators=[
		validators.Email(),
		validators.DataRequired(),
		validators.Length(max=128)
	])
	password = wtforms.PasswordField("Password", validators=[
		validators.DataRequired(),
		validators.Length(min=6, max=32)
	])
	remember_me = wtforms.BooleanField("Remember me", default=False)

	def __init__(self, *args, **kwargs):
		"""Initialize LoginForm. Override from FlaskForm __init__

		Arguments:
			*args -- Passed arguments
			**kwargs -- Passed keyword arguments
		"""

		self.user = None
		super(LoginForm, self).__init__(*args, **kwargs)

	def validate(self):
		"""Validate login data. Override from FlaskForm validate()

		Returns:
			Boolean -- Return validation result
		"""

		if not super(LoginForm, self).validate():
			return False

		self.user = User.autheticate(self.email.data, self.password.data)
		if not self.user:
			self.email.errors.append("Invalid email or password")
			return False

		return True
