# -*- coding: utf-8 -*-

"""Models in base modules

Author:
	@CakJuice <hd.brandoz@gmail.com>
"""

from datetime import datetime
from smtplib import SMTPException

from flask import url_for
from flask_mail import Message
from app import app, db, argon2, login_manager, mail
from models import BaseModel
from helpers import generate_random_string, generate_slug as slugify

class User(db.Model, BaseModel):
	"""User model, mixin inherit db.Model from flask_sqlalchemy & BaseModel from models.py
	"""

	__tablename__ = 'cj_base_user'

	STATUS_DELETED = -1
	STATUS_NOT_ACTIVE = 0
	STATUS_ACTIVE = 1

	def generate_slug(self):
		"""Generate slug from name value

		Returns:
			Boolean|None -- Result from helpers.generate_slug
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
	status = db.Column(db.SmallInteger, default=STATUS_NOT_ACTIVE,
		doc="1 = active, 0 = not active, -1 = deleted")
	is_admin = db.Column(db.Boolean, default=False)
	verify_code = db.Column(db.String(32), default=generate_random_string(32))
	created_at = db.Column(db.DateTime, default=datetime.now)
	updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
	last_request_at = db.Column(db.DateTime)
	# mail_outgoing_create_by = db.relationship('MailOutgoing', backref='mail_outgoing_created_by',
	# 	lazy='dynamic', foreign_keys='{}.created_by'.format(MailOutgoing.__tablename__))
	# mail_outgoing_update_by = db.relationship('MailOutgoing', backref='mail_outgoing_update_by',
	# 	lazy='dynamic', foreign_keys='{}.update_by'.format(MailOutgoing.__tablename__))

	def __repr__(self):
		"""Representation name
		"""

		return '<User: {}>'.format(self.name)

	# flask-login interface
	def get_id(self):
		return self.id

	def is_authenticated(self):
		return True

	def is_active(self):
		return self.status == User.STATUS_ACTIVE

	def is_anonymous(self):
		return False

	@staticmethod
	def make_password(plaintext):
		"""Create hash password from plaintext

		Arguments:
			plaintext {String} -- Plaintext which to be hashed

		Returns:
			String -- Hash result
		"""
		return argon2.generate_password_hash(plaintext)

	def check_password(self, raw_password):
		"""Verify input password with password_hash

		Arguments:
			raw_password {String} -- Input password which to be verified

		Returns:
			Boolean -- Verify result
		"""
		return argon2.check_password_hash(self.password_hash, raw_password)

	@staticmethod
	def authenticate(email, password):
		"""Check user authenticate when login

		Arguments:
			email {String} -- Input email from user
			password {String} -- Input password from user

		Returns:
			Recordset|Boolean -- Auth result, if user found then return user data, else return false
		"""
		user = User.query.filter_by(email=email, status=User.STATUS_ACTIVE).first()
		if user and user.check_password(password):
			return user
		return False

	def set_verified(self):
		"""Update data status user when user verified account
		"""
		self.status = User.STATUS_ACTIVE
		self.save()

	def resend_verification_mail(self):
		"""Generate new verification code then resend verification mail
		"""

		self.verify_code = generate_random_string(32)
		self.save()
		self.send_verification_mail()

	def send_verification_mail(self):
		"""Sending verification email after user signup.
		"""

		body = """Hi, {0}.
Terima kasih sudah medaftarkan diri disini.
Silahkan buka link {1} untuk verifikasi pendaftaran.

Terima kasih.
		""".format(self.name, url_for('base.verify', verify_code=self.verify_code, _external=True))

		body_html = """<p>Hi, {0}</p>
<p>Terima kasih sudah mendaftarkan diri disini.</p>
<p>Silahkan buka link <a href="{1}" target="_blank">{1}</a> untuk verifikasi pendaftaran.</p>
<br>
<p>Terima kasih.</p>
		"""

		outgoing_mail = MailOutgoing(
			subject="Verifikasi Pendaftaran User",
			email_to=self.email,
			body=body,
			body_html=body_html
		)
		outgoing_mail.send_email()

@login_manager.user_loader
def _user_loader(user_id):
	return User.query.get(int(user_id))

class MailOutgoing(db.Model, BaseModel):
	"""MailOutgoing model, mixin inherit db.Model from flask_sqlalchemy & BaseModel from models.py
	"""

	__tablename__ = 'cj_base_mail_outgoing'

	STATUS_CANCELED = -1
	STATUS_OUTGOING = 0
	STATUS_SEND = 1
	STATUS_RECEIVED = 2
	STATUS_FAILED = 3

	id = db.Column(db.Integer, primary_key=True)
	subject = db.Column(db.String(255), nullable=False)
	email_from = db.Column(db.String(255), nullable=False, default=app.config['MAIL_USERNAME'])
	email_to = db.Column(db.Text, nullable=False)
	email_cc = db.Column(db.Text)
	body = db.Column(db.Text, nullable=False)
	body_html = db.Column(db.Text)
	status = db.Column(db.SmallInteger, default=STATUS_OUTGOING,
		doc="-1 = canceled, 0 = outgoing, 1 = send, 2 = received, 3 = delivery failed")
	send_at = db.Column(db.DateTime)
	created_at = db.Column(db.DateTime, default=datetime.now)
	updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

	def __repr__(self):
		"""Representation name
		"""
		return '<MailOutgoing: {}>'.format(self.subject)

	def send_email(self):
		"""Sending email then update status to STATUS_SEND when success
		"""
		message = Message(
			subject=self.subject,
			body=self.body,
			html=self.body_html,
			sender=self.email_from,
			recipients=[self.email_to]
		)

		try:
			mail.send(message)
			self.status = self.STATUS_SEND
			self.send_at = datetime.now()
			self.save()
		except SMTPException:
			self.status = self.STATUS_FAILED
			self.save()
