from django.db import models

# Blogpost creation
class Post(models.Model):

	title = models.CharField(max_length = 200)
	pub_date = models.DateTimeField()
	text = models.TextField()