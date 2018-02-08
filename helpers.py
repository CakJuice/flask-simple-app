# -*- coding: utf-8 -*-

"""
# Various helpers library of flask app
# @author: @CakJuice <hd.brandoz@gmail.com>
"""

import re, string, random

def slugify(raw_string):
	"""
	# Get slug string pattern
	# @param raw_string (string): string to get slug
	# @return (string): result of slug string
	"""
	return re.sub(r'[^\w]+', '-', raw_string).lower()

def generate_slug(cls, raw_string):
	"""
	# Get slug string pattern
	# First must check to database, because slug usually unique
	# If slug value same with record in db, slug string will add increment number
	# @param raw_string (string): string to get slug
	# @return (string): result of slug string
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
		else:
			return "{0}-1".format(slug)
	else:
		return slug

def generate_random_string(length):
	"""
	# Generate random string
	# @param length (int): length of random string
	# @return (string): random result
	"""
	char_list = string.ascii_uppercase + string.digits + string.ascii_lowercase
	return ''.join(random.choice(char_list) for _ in range(length))