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

	# Known bug: Id increments seem quite random. May have to fix this.

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

	def testCreatePost(self):

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Check the response code
		response = self.client.get('/admin/blogengine/post/add/', follow = True)
		self.assertEquals(response.status_code, 200)

		# Create a test post
		response = self.client.post('/admin/blogengine/post/add/', {
			'title': 'Test post',
			'text': 'This is a test post for testing.',
			'pubDate_0': '2015-12-30',
			'pubDate_1': '12:56:05'
			},
			follow = True)
		self.assertEquals(response.status_code, 200)

		# Check added successfully
		self.assertTrue('added successfully' in smart_text(response.content))

		# Check that the post is now in the database
		allPosts = Post.objects.all()
		self.assertEquals(len(allPosts), 1)

	def testEditPost(self):

		# Create the post
		post = Post()
		post.title = 'Test post number 1'
		post.text = 'This is the first test post for testing.'
		post.pubDate = timezone.now()
		post.save()

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Edit the post
		response = self.client.post('/admin/blogengine/post/3/change/', {
			'title': 'Test post number 2',
			'text': 'This is the second test post for testing.',
			'pubDate_0': '2015-12-30',
			'pubDate_1': '12:56:05'
        },
        follow = True
        )
		self.assertEquals(response.status_code, 200)

		# Check that the changes were successfull
		self.assertTrue('changed successfully' in smart_text(response.content))

		# Check post amended
		allPosts = Post.objects.all()
		self.assertEquals(len(allPosts), 1)
		onlyPost = allPosts[0]
		self.assertEquals(onlyPost.title, 'Test post number 2')
		self.assertEquals(onlyPost.text, 'This is the second test post for testing.')

	def testDeletePost(self):
		# Creates the post
		post = Post()

		# Sets the attributes of the post
		post.title = 'Test post'
		post.text = 'This is a test post for testing.'
		post.pubDate = timezone.now()
		post.save()

		# Check that a new post is saved
		allPosts = Post.objects.all()
		self.assertEquals(len(allPosts), 1)

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Delete the post
		response = self.client.post('/admin/blogengine/post/2/delete/', {
			'post': 'yes'
			}, follow = True)
		self.assertEquals(response.status_code, 200)

		# Check that the post was deleted successfully
		self.assertTrue('deleted successfully' in smart_text(response.content))
		