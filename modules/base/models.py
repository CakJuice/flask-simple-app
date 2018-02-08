# -*- coding: utf-8 -*-

"""
# Data model in base modules
# @author: @CakJuice <hd.brandoz@gmail.com>
"""

from datetime import datetime

from app import app, db, argon2
from models import BaseModel
from helpers import generate_random_string, generate_slug as slugify

class User(db.Model, BaseModel):
	__tablename__ = 'cj_base_user'

	def generate_slug(self):
		"""
		# Generate slug from name
		# @param self (class): class object
		# @return (string | None): result from helpers.generate_slug
		"""
		name = self.current_parameters.get('name')
		if name:
			return slugify(User, name)
		return None

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(128), nullable=False, unique=True)
	password_hash = db.Column(db.String(255), nullable=False)
	name = db.Column(db.String(100), nullable=False)
	slug = db.Column(db.String(128), nullable=False, unique=True, default=generate_slug)
	status = db.Column(db.SmallInteger, default=0, doc="1 = active, 0 = need activated, -1 = non-active")
	is_admin = db.Column(db.Boolean, default=False)
	verify_code = db.Column(db.String(32), default=generate_random_string(32))
	created_at = db.Column(db.DateTime, default=datetime.now)
	updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
	last_request_at = db.Column(db.DateTime)

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)

	def __str__(self):
		return '<User: {}>'.format(self.name)

	@staticmethod
	def make_password(plaintext):
		"""
		# Create hash password from plaintext
		# @param plaintext (string): plaintext which to be hashed
		# @return (string): hash result
		"""
		return argon2.generate_password_hash(plaintext)

	def check_password(self, raw_password):
		"""
		# Verify input password with password_hash
		# @param self: instantiate class object
		# @param raw_password (string): input password which to be verified
		# @return (boolean): verify result
		"""
		return argon2.check_password_hash(self.password_hash, raw_password)

	@staticmethod
	def authenticate(email, password):
		"""
		# Check user when login
		# @param email (string): input email from user
		# @param password (string): input password from user
		# @return (recordset | boolean): auth result, if user found then return user data, else return false
		"""
		user = User.query.filter_by(email=email).first()
		if user and user.check_password(password):
			return user
		return False

	def set_verified(self):
		"""
		# Update data status user when user verified account
		# @param self: instantiate class object
		"""
		self.status = 1
		self.save()