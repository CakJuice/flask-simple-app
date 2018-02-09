from app import db

class BaseModel(object):
	def save(self):
		db.session.add(self)
		db.session.commit()
