# -*- coding: utf-8 -*-

"""Mail model in base modules

Author:
	@CakJuice <hd.brandoz@gmail.com>
"""

from datetime import datetime
from smtplib import SMTPException

from flask import g
from flask_mail import Message
from app import app, db, mail
from models import BaseModel
from .user import User

class MailOutgoing(db.Model, BaseModel):
    """MailOutgoing model, mixin inherit `db.Model` from `flask_sqlalchemy` & `BaseModel` from models.py
    """

    __tablename__ = 'cj_base_mail_outgoing'

    STATUS_CANCELED = -1
    STATUS_OUTGOING = 0
    STATUS_SEND = 1
    STATUS_RECEIVED = 2
    STATUS_FAILED = 3

    def generate_user_id(self):
        """Generate user id. If mail created manually, user id generated from session.
        If mail created automatically, user id generated from user who is_admin

        Returns:
            Int -- Generated user id
        """
        if hasattr(g, 'user') and hasattr(g.user, 'id') and g.user.id:
            return g.user.id
        user = User.query.filter_by(is_admin=True).first()
        return user.id

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
    created_by = db.Column(db.Integer, db.ForeignKey('{}.id'.format(User.__tablename__), ondelete='CASCADE'),
        default=generate_user_id)
    updated_by = db.Column(db.Integer, db.ForeignKey('{}.id'.format(User.__tablename__), ondelete='CASCADE'),
        default=generate_user_id, onupdate=generate_user_id)

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
