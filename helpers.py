# -*- coding: utf-8 -*-

"""Various helpers library of flask app

Author:
	@CakJuice <hd.brandoz@gmail.com>
"""

from re import sub
from string import ascii_uppercase, ascii_lowercase, digits
from random import choice

def slugify(raw_string):
	"""Get slug string pattern

	Arguments:
		raw_string {String} -- String to get slug

	Returns:
		String -- Result of slug string
	"""
	return sub(r'[^\w]+', '-', raw_string).lower()

def generate_slug(cls, raw_string):
	"""Get slug string pattern. First must check to database, because slug usually unique. \
If slug value same with record in db, slug string will add increment number

	Arguments:
		raw_string {String} -- String to get slug

	Returns:
		String -- Result of slug string
	"""
	if not hasattr(cls, 'slug'):
		return None

	slug = slugify(raw_string)
	obj = getattr(cls, 'slug')
	model = cls.query.filter(obj.startswith(slug)).order_by(obj.desc()).first()
	if model:
		idx_slug = model.slug.split('-')[-1]
		if idx_slug.isdigit():
			idx_new = int(idx_slug) + 1
			return "{0}-{1}".format(slug, idx_new)

		return "{0}-1".format(slug)

	return slug

def generate_random_string(length):
	"""Generate random string

	Arguments:
		length {Int} -- Length of random string

	Returns:
		String -- Random result
	"""
	char_list = ascii_uppercase + digits + ascii_lowercase
	return ''.join(choice(char_list) for _ in range(length))
