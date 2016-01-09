from django.db import models

# Blogpost creation
class Post(models.Model):

	# Model specifications
	title = models.CharField(max_length = 200)
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
