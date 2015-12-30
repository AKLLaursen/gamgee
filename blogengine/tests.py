from django.test import TestCase
from django.utils import timezone
from blogengine.models import Post

# Test for blogpost creation
class PostTest(TestCase):

	def testCreatePost(self):

		# Creates the post
		post = Post()

		# Sets the attributes of the post
		post.title = 'Test post'
		post.text = 'This is a test post for testing.'
		post.pubDate = timezone.now()

		# Saves the post
		post.save()

		# Checks that the post can be found
		allPosts = Post.objects.all()
		self.assertEquals(len(allPosts), 1)
		onlyPost = allPosts[0]
		self.assertEquals(onlyPost, post)

		# Checks the attributes of the post
		self.assertEquals(onlyPost.title, 'Test post')
		self.assertEquals(onlyPost.text, 'This is a test post for testing.')
		self.assertEquals(onlyPost.pubDate.day, post.pubDate.day)
		self.assertEquals(onlyPost.pubDate.month, post.pubDate.month)
		self.assertEquals(onlyPost.pubDate.year, post.pubDate.year)
		self.assertEquals(onlyPost.pubDate.hour, post.pubDate.hour)
		self.assertEquals(onlyPost.pubDate.minute, post.pubDate.minute)
		self.assertEquals(onlyPost.pubDate.second, post.pubDate.second)
