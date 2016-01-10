from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Category creation
class Category(models.Model):

	name = models.CharField(max_length = 200)
	description = models.TextField()
	slug = models.SlugField(max_length = 40, unique = True, blank = True, null = True)

	def save(self):

		if not self.slug:
			self.slug = slugify(self.name)

		super(Category, self).save()

	def get_absolute_url(self):
		return '/category/{0}/'.format(self.slug)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'categories'

# Blogpost creation
class Post(models.Model):

	# Model specifications
	title = models.CharField(max_length = 200)
	author = models.ForeignKey(User)
	category = models.ForeignKey(Category, blank = True, null = True)
	pub_date = models.DateTimeField()
	text = models.TextField()
	slug = models.SlugField(max_length = 40, unique = True)

	# Define url for each post. (Possibly change this to have 0 in front of single number elements.)
	def get_abs_url(self):
		return '/{0}/{1}/{2}/{3}/'.format(self.pub_date.year, self.pub_date.month, self.pub_date.day, self.slug)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-pub_date']
