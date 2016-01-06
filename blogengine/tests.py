import markdown

from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from django.utils.encoding import smart_text 
from blogengine.models import Post

# Test for blogpost creation
class PostTest(TestCase):

	def test_create_post(self):

		# Creates the post
		post = Post()

		# Sets the attributes of the post
		post.title = 'Test post'
		post.text = 'This is a test post for testing.'
		post.pub_date = timezone.now()

		# Saves the post
		post.save()

		# Checks that the post can be found
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Checks the attributes of the post
		self.assertEquals(only_post.title, 'Test post')
		self.assertEquals(only_post.text, 'This is a test post for testing.')
		self.assertEquals(only_post.pub_date.day, post.pub_date.day)
		self.assertEquals(only_post.pub_date.month, post.pub_date.month)
		self.assertEquals(only_post.pub_date.year, post.pub_date.year)
		self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
		self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
		self.assertEquals(only_post.pub_date.second, post.pub_date.second)

# Test login on the admin page
class AdminTest(LiveServerTestCase):

	# Known bug: Id increments seem quite random. May have to fix this.

	# Load fixtures
	fixtures = ['users.json']

	# Set-up client
	def set_up(self):
		self.client = Client()

	def test_log_in(self):

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

	def test_log_out(self):

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

	def test_create_post(self):

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Check the response code
		response = self.client.get('/admin/blogengine/post/add/', follow = True)
		self.assertEquals(response.status_code, 200)

		# Create a test post
		response = self.client.post('/admin/blogengine/post/add/', {
			'title': 'Test post',
			'text': 'This is a test post for testing.',
			'pub_date_0': '2015-12-30',
			'pub_date_1': '12:56:05'
			},
			follow = True)
		self.assertEquals(response.status_code, 200)

		# Check added successfully
		self.assertTrue('added successfully' in smart_text(response.content))

		# Check that the post is now in the database
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

	def test_edit_post(self):

		# Create the post
		post = Post()
		post.title = 'Test post number 1'
		post.text = 'This is the first test post for testing.'
		post.pub_date = timezone.now()
		post.save()

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Get the ID of the post, as this is subject to change
		all_posts = Post.objects.all()
		post_id = all_posts[0].id

		# Edit the post
		response = self.client.post(('/admin/blogengine/post/' + str(post_id) + '/change/'), {
			'title': 'Test post number 2',
			'text': 'This is the second test post for testing.',
			'pub_date_0': '2015-12-30',
			'pub_date_1': '12:56:05'
        },
        follow = True
        )
		self.assertEquals(response.status_code, 200)

		# Check that the changes were successfull
		self.assertTrue('changed successfully' in smart_text(response.content))

		# Check post amended. Get all post objects again to make sure nothing has changed.
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post.title, 'Test post number 2')
		self.assertEquals(only_post.text, 'This is the second test post for testing.')

	def test_delete_post(self):

		# Creates the post
		post = Post()

		# Sets the attributes of the post
		post.title = 'Test post'
		post.text = 'This is a test post for testing.'
		post.pub_date = timezone.now()
		post.save()

		# Check that a new post is saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Get post ID
		post_id = all_posts[0].id

		# Delete the post
		response = self.client.post(('/admin/blogengine/post/' + str(post_id) + '/delete/'), {
			'post': 'yes'
			}, follow = True)
		self.assertEquals(response.status_code, 200)

		# Check that the post was deleted successfully
		self.assertTrue('deleted successfully' in smart_text(response.content))

# Test for Views
class PostViewTest(LiveServerTestCase):

	# Set-up client
	def set_up(self):
		self.client = Client()

	def test_index(self):

		#Create a post
		post = Post()

		# Sets the attributes of the post
		post.title = 'Test post'
		post.text = 'This is a test [post for testing.](http://127.0.0.1:8000/)'
		post.pub_date = timezone.now()
		post.save()

		# Check that a new post is saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

		# Get the index
		response = self.client.get('/', follow = True)
		self.assertEquals(response.status_code, 200)

		# Check that the post title is in the reponse
		self.assertTrue(post.title in smart_text(response.content))

		# Check that the post text is in the response
		self.assertTrue(markdown.markdown(post.text) in smart_text(response.content))

		# Check that the post date is in the response
		self.assertTrue(str(post.pub_date.year) in smart_text(response.content))
		self.assertTrue(post.pub_date.strftime('%b') in smart_text(response.content))
		self.assertTrue(str(post.pub_date.day) in smart_text(response.content))

		# Check the link is marked up properly
		self.assertTrue('<a href="http://127.0.0.1:8000/">post for testing.</a>' in smart_text(response.content))
