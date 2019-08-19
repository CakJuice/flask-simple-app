# -*- coding: utf-8 -*-

""" Mail model in base modules

Author: @CakJuice <hd.brandoz@gmail.com>
"""

from datetime import datetime
from smtplib import SMTPException

from flask_mail import Message

from app import app, db, mail
from models import BaseModel
from settings import Configuration


class Email(db.Model, BaseModel):
    """ MailOutgoing model, mixin inherit `db.Model` from `flask_sqlalchemy` & `BaseModel` from models.py
    """

    __tablename__ = Configuration.TABLE_PREFIX + 'base_email'

    STATE_CHOICES = (
        (0, "Draft"),
        (1, "Ready"),
        (2, "Sent"),
        (3, "Received"),
        (4, "Failed")
    )

    def get_state_value(self, name):
        """ To get state value based from name as param.
        :param name: String - State name.
        :return: Int - State value.
        """
        for choice in self.STATE_CHOICES:
            if name.lower() == choice[1].lower():
                return choice[0]

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    email_from = db.Column(db.String(255), nullable=False, default=app.config['MAIL_USERNAME'])
    email_to = db.Column(db.Text, nullable=False)
    email_cc = db.Column(db.Text)
    body = db.Column(db.Text, nullable=False)
    body_html = db.Column(db.Text)
    state = db.Column(db.SmallInteger, default=get_state_value('draft'),
                       doc="0 = Draft, 1 = Ready, 2 = Sent, 3 = Received, 4 = Failed")
    send_at = db.Column(db.DateTime)

    def __repr__(self):
        """ Representation name """
        return '<MailOutgoing: %s>' % self.subject

    def send_email(self):
        """ Sending email then update status to STATUS_SEND when success """
        message = Message(
            subject=self.subject,
            body=self.body,
            html=self.body_html,
            sender=self.email_from,
            recipients=[self.email_to]
        )

        try:
            mail.send(message)
            self.status = self.get_state_value('sent')
            self.send_at = datetime.now()
            self.save()
        except SMTPException:
            self.status = self.get_state_value('failed')
            self.save()
