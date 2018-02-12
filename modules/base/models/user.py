# -*- coding: utf-8 -*-

"""User model in base modules

Author:
	@CakJuice <hd.brandoz@gmail.com>
"""

from datetime import datetime

from flask import url_for
from app import db, argon2, login_manager
from models import BaseModel
from helpers import generate_random_string, generate_slug as slugify

class User(db.Model, BaseModel):
    """User model, mixin inherit `db.Model` from `flask_sqlalchemy` & `BaseModel` from models.py
    """

    __tablename__ = 'cj_base_user'

    STATUS_DELETED = -1
    STATUS_NOT_ACTIVE = 0
    STATUS_ACTIVE = 1

    VERIFY_BODY = """Hi, {0}.
Terima kasih sudah medaftarkan diri disini.
Silahkan buka link {1} untuk verifikasi pendaftaran.

Terima kasih.
        """

    VERIFY_BODY_HTML = """<p>Hi, {0}</p>
<p>Terima kasih sudah mendaftarkan diri disini.</p>
<p>Silahkan buka link <a href="{1}" target="_blank">{1}</a> untuk verifikasi pendaftaran.</p>
<br>
<p>Terima kasih.</p>
        """

    def generate_slug(self):
        """Generate slug from name value

        Returns:
            Boolean|None -- Result from helpers.generate_slug
        """
        name = self.current_parameters.get('name')
        if name:
            return slugify(User, name)
        return None

    def check_status_admin(self):
        """Check status `is_admin` user. If `is_admin` already available it will be return `False`

        Returns:
            Boolean -- Result user query
        """
        user = User.query.filter_by(is_admin=True).first()
        if user is None:
            return True
        return False

    def check_status_active(self):
        """Check `status` user. If `self.is_admin` then `status' auto active

        Returns:
            Int -- Result status active
        """
        is_admin_check = self.current_parameters.get('is_admin', False)
        if is_admin_check:
            return User.STATUS_ACTIVE
        return User.STATUS_NOT_ACTIVE

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(128), nullable=False, unique=True, default=generate_slug)
    is_admin = db.Column(db.Boolean, default=check_status_admin)
    status = db.Column(db.SmallInteger, default=check_status_active,
        doc="1 = active, 0 = not active, -1 = deleted")
    verify_code = db.Column(db.String(32), default=lambda: generate_random_string(32))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    last_request_at = db.Column(db.DateTime)

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
        """Verify input password with `password_hash`

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
        from .mail import MailOutgoing

        outgoing_mail = MailOutgoing(
            subject="Verifikasi Pendaftaran User",
            email_to=self.email,
            body=self.VERIFY_BODY.format(self.name, url_for('base.verify',
                verify_code=self.verify_code, _external=True)),
            body_html=self.VERIFY_BODY_HTML.format(self.name,
                url_for('base.verify', verify_code=self.verify_code, _external=True))
        )
        outgoing_mail.send_email()

@login_manager.user_loader
def _user_loader(user_id):
    return User.query.get(int(user_id))
