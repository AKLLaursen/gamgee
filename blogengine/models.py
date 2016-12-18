from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.core.cache import cache

# Category model
class Category(models.Model):

	name = models.CharField(max_length = 200)
	description = models.TextField()
	slug = models.SlugField(max_length = 40, unique = True, blank = True, null = True)

	def save(self, *args, **kwargs):

		if not self.slug:
			self.slug = slugify(str(self.name))

		super(Category, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return '/category/{0}/'.format(self.slug)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'categories'

# Tag model
class Tag(models.Model):

	name = models.CharField(max_length = 200)
	description = models.TextField()
	slug = models.SlugField(max_length = 40, unique = True, blank = True, null = True)

	def save(self, *args, **kwargs):

		if not self.slug:
			self.slug = slugify(str(self.name))

		super(Tag, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return "/tag/%s/" % (self.slug)

	def __str__(self):
		return self.name

# Blogpost model
class Post(models.Model):

	# Model specifications
	title = models.CharField(max_length = 200)
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	category = models.ForeignKey(Category, blank = True, null = True, on_delete = models.CASCADE)
	tags = models.ManyToManyField(Tag,  blank = True, null = True)
	pub_date = models.DateTimeField()
	text = models.TextField()
	slug = models.SlugField(max_length = 40, unique = True)
	site = models.ForeignKey(Site, on_delete = models.CASCADE)

	# Define url for each post. (Possibly change this to have 0 in front of single number elements.)
	def get_absolute_url(self):
		return '/{0}/{1}/{2}/{3}/'.format(self.pub_date.year, self.pub_date.month, self.pub_date.day, self.slug)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-pub_date']

# Define signals function
def new_post(sender, instance, created, **kwargs):
    cache.clear()

# Set up signals
post_save.connect(new_post, sender = Post)