# -*- coding: utf-8 -*-

""" Models helper.

Author: @CakJuice <hd.brandoz@gmail.com>
"""

from datetime import datetime

from flask import g

from app import db
from modules.base.models.user import User


class BaseModel(object):
    """ Mixin class with db.Model """

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

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    created_by = db.Column(db.Integer, db.ForeignKey('{}.id'.format(User.__tablename__), ondelete='CASCADE'),
                           default=generate_user_id)
    updated_by = db.Column(db.Integer, db.ForeignKey('{}.id'.format(User.__tablename__), ondelete='CASCADE'),
                           default=generate_user_id, onupdate=generate_user_id)

    def save(self):
        """Save (commit) data to database
        """
        db.session.add(self)
        db.session.commit()
