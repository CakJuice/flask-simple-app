import os

from flask import request
from wtforms import validators
from wtforms.compat import string_types

def get_file_size(file):
	file.seek(0, os.SEEK_END)
	return file.tell()

class FileAllowed(object):
	def __init__(self, extensions=[], message=None):
		"""
		# @param extensions (list): list of allowed extension of uploaded file
		# @oaram message (string): custom message when this validation fails
		"""
		self.extensions = extensions
		self.message = message

	def __call__(self, form, field):
		"""
		# Call when request post data from some form
		# @param form (object/class): form which some field has this validators 
		# @param field (object/class): field which has this validators
		"""
		if field.data and isinstance(field.data, string_types) and field.data.strip():
			if len(self.extensions) > 0:
				status = False
				for ext in self.extensions:
					if field.data.endswith(ext):
						status = True
						break

				if not status:
					if self.message is None:
						message = "Hanya bisa upload " + ", ".join(self.extensions)
					else:
						message = self.message

					field.errors = []
					raise validators.StopValidation(message)

class MaxFileSizeAllowed(object):
	def __init__(self, max_size=0, message=None):
		"""
		# @param max_size (integer): size of uploaded file, in KB
		# @param message (string): custom message when this validation fails
		"""
		self.max_size = max_size
		self.message = message

	def __call__(self, form, field):
		"""
		# Call when request post data from some form
		# @param form (object/class): form which some field has this validators 
		# @param field (object/class): field which has this validators
		"""
		if field.data and field.name in request.files:
			file_size = get_file_size(request.files[field.name]) / 1000.0
			if file_size > self.max_size:
				if self.message is None:
					message = "Max. ukuran file {} KB.".format(self.max_size,)
				else:
					message = self.message

				field.errors = []
				raise validators.StopValidation(message)

class SameValue(object):
	def __init__(self, same_field, message=None):
		"""
		# @param same_field (string): other field name to compare value
		# @param message (string): custom message when this validation fails
		"""
		if isinstance(same_field, string_types):
			self.same_field = same_field

		self.message = message

	def __call__(self, form, field):
		"""
		# Call when request post data from some form
		# @param form (object/class): form which some field has this validators 
		# @param field (object/class): field which has this validators
		"""
		if field.data and isinstance(field.data, string_types) and \
			field.data.strip():
				if self.same_field not in form.data:
					message = "Terjadi kesalahan, hubungi administrator!"
					field.errors = []
					raise validators.StopValidation(message)

				if form.data[self.same_field] != field.data:
					if self.message is None:
						message = "Data tidak sama dengan {}!".format(self.same_field)
					else:
						message = self.message
					field.errors = []
					raise validators.StopValidation(message)

class UniqueValue(object):
	def __init__(self, model, field_name, message=None):
		self.model = model
		self.field_name = field_name
		self.message = message

	def __call__(self, form, field):
		if not hasattr(self.model, self.field_name):
			message = "Terjadi kesalahan, hubungi administrator!"
			field.errors = []
			raise validators.StopValidation(message)
		
		if field.data and isinstance(field.data, string_types) and \
			field.data.strip():
				obj = getattr(self.model, self.field_name)
				user = self.model.query.filter(obj == field.data).first()
				if user:
					field.errors = []
					if self.message is None:
						message = "Data {} sudah ada!".format(self.field_name)
					else:
						message = self.message
					raise validators.StopValidation(message)