from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from django.utils.encoding import smart_text 
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

# Test login on the admin page
class AdminTest(LiveServerTestCase):

	# Load fixtures
	fixtures = ['users.json']

	# Set-up client
	def setUp(self):
		self.client = Client()

	def testLogIn(self):

		# Get the login page, note that redirection has to be given explicitly, otherwise a 302 response code is given.
		response = self.client.get('/admin/', follow = True)

		# Check the response code
		self.assertEquals(response.status_code, 200)

		# Check the response text, note that in python 3 byte and str is two different data types. Convertion is easily handled using smart_text.
		self.assertTrue('Log in' in smart_text(response.content))

		# Log the user in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Check the response code again
		response = self.client.get('/admin/', follow = True)
		self.assertEquals(response.status_code, 200)

		# Check the response text again
		self.assertTrue('Log out' in smart_text(response.content))

	def testLogOut(self):

		# Log the user in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Check the response code
		response = self.client.get('/admin/', follow = True)
		self.assertEquals(response.status_code, 200)

		# Check the response text
		self.assertTrue('Log out' in smart_text(response.content))

		# Log out
		self.client.logout()

		# Check the response code again
		response = self.client.get('/admin/', follow = True)
		self.assertEquals(response.status_code, 200)

		# Check the response text again
		self.assertTrue('Log in' in smart_text(response.content))
