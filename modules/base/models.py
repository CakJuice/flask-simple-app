import random
import string
from datetime import datetime

from app import app, db, argon2
from models import BaseModel
from helpers import generate_slug as slugify

class User(db.Model, BaseModel):
	__tablename__ = 'cj_base_user'

	def generate_slug(context):
		name = context.current_parameters.get('name')
		if name:
			return slugify(User, name)
		return None

	def generate_verify_code(context):
		char_list = string.ascii_uppercase + string.digits + string.ascii_lowercase
		return ''.join(random.choice(char_list) for _ in range(32))

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(128), nullable=False, unique=True)
	password_hash = db.Column(db.String(255), nullable=False)
	name = db.Column(db.String(100), nullable=False)
	slug = db.Column(db.String(128), nullable=False, unique=True, default=generate_slug)
	status = db.Column(db.SmallInteger, default=0, doc="1 = active, 0 = need activated, -1 = non-active")
	is_admin = db.Column(db.Boolean, default=False)
	verify_code = db.Column(db.String(32), default=generate_verify_code)
	created_at = db.Column(db.DateTime, default=datetime.now)
	updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
	last_request_at = db.Column(db.DateTime)

	def __init__(self, *args, **kwargs):
		return super(User, self).__init__(*args, **kwargs)

	def __str__(self):
		return '<User: {}>'.format(self.name)

	@staticmethod
	def make_password(plaintext):
		return argon2.generate_password_hash(plaintext)

	def check_password(self, raw_password):
		return argon2.check_password_hash(self.password_hash, raw_password)

	@staticmethod
	def authenticate(email, password):
		user = User.query.filter_by(email=email).first()
		if user and user.check_password(password):
			return user
		return False

	def set_verified(self):
		self.status = 1
		self.save()