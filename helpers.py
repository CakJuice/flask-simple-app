import re

def slugify(raw_string):
	return re.sub(r'[^\w]+', '-', raw_string).lower()

def generate_slug(cls, raw_string):
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