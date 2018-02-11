# -*- coding: utf-8 -*-

"""Set of custom validation for flask_wtf

Author:
	@CakJuice <hd.brandoz@gmail.com>
"""

import os

from flask import request
from wtforms import validators
from wtforms.compat import string_types

def get_file_size(file):
	"""Get file size when uploaded file

	Arguments:
		file {File} -- Uploaded file

	Returns:
		Int -- File size
	"""
	file.seek(0, os.SEEK_END)
	return file.tell()

class FileAllowed(object):
	"""To set which file extension to be allowed when uploading files. \
If file extension is not in extension list, it will be raise an exception
	"""

	def __init__(self, extensions=[], message=None):
		"""Instantiate class object

		Keyword Arguments:
			extensions {List} -- List of allowed extension of uploaded file (default: {[]})
			message {String} -- Custom message when this validation fails (default: {None})
		"""
		self.extensions = extensions
		self.message = message

	def __call__(self, form, field):
		"""Call when request post data from some form. \
If this validation fails, it will be raise StopValidation

		Arguments:
			form {Object/Class} -- Form which some field has this validators
			field {Object/Class} -- Field which has this validators

		Raises:
			validators.StopValidation -- Raise when validation fails
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
	"""To set max size of file when uploading files. \
If upload file size is bigger this validations fails
	"""

	def __init__(self, max_size=0, message=None):
		"""Instantiate class object

		Keyword Arguments:
			max_size {Int} -- Size of uploaded file, in KB (defualt: {0})
			message {String} -- Custom message when this validation fails (default: {None})
		"""
		self.max_size = max_size
		self.message = message

	def __call__(self, form, field):
		"""Call when request post data from some form. \
If this validation fails, it will be raise StopValidation

		Arguments:
			form {Object/Class} -- Form which some field has this validators
			field {Object/Class} -- Field which has this validators

		Raises:
			validators.StopValidation -- Raise when validation fails
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
	"""To check data from other field. \
The data must be same or will raise an exception
	"""

	def __init__(self, same_field, message=None):
		"""Instantiate class object

		Keyword Arguments:
			same_field {String} -- Other field name to compare value
			message {String} -- Custom message when this validation fails (default: {None})
		"""
		if isinstance(same_field, string_types):
			self.same_field = same_field

		self.message = message

	def __call__(self, form, field):
		"""Call when request post data from some form. \
If this validation fails, it will be raise StopValidation

		Arguments:
			form {Object/Class} -- Form which some field has this validators
			field {Object/Class} -- Field which has this validators

		Raises:
			validators.StopValidation -- Raise when validation fails
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
		"""Instantiate class object

		Keyword Arguments:
			model {Object/Class} -- Model class which will be checking value
			field_name {String} -- Field name of model which will be checking value
			message {String} -- Custom message when this validation fails (default: {None})
		"""
		self.model = model
		self.field_name = field_name
		self.message = message

	def __call__(self, form, field):
		"""Call when request post data from some form. \
If this validation fails, it will be raise StopValidation

		Arguments:
			form {Object/Class} -- Form which some field has this validators
			field {Object/Class} -- Field which has this validators

		Raises:
			validators.StopValidation -- Raise when validation fails
		"""
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
