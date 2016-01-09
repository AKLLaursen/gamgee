import markdown

from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from django.utils.encoding import smart_text 
from blogengine.models import Post
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

# Test for blogpost creation
class PostTest(TestCase):

	def test_create_post(self):

		# Create a blog author
		author = User.objects.create_user('TestUser', 'test@user.com', 'password')
		author.save

		# Creates the post
		post = Post()

		# Sets the attributes of the post
		post.title = 'Test post'
		post.author = author
		post.pub_date = timezone.now()
		post.text = 'This is a test post for testing.'
		post.slug = 'test-post'

		# Saves the post
		post.save()

		# Checks that the post can be found
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Checks the attributes of the post
		self.assertEquals(only_post.title, 'Test post')
		self.assertEquals(only_post.author.username, 'TestUser')
		self.assertEquals(only_post.author.email, 'test@user.com')
		self.assertEquals(only_post.pub_date.day, post.pub_date.day)
		self.assertEquals(only_post.pub_date.month, post.pub_date.month)
		self.assertEquals(only_post.pub_date.year, post.pub_date.year)
		self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
		self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
		self.assertEquals(only_post.pub_date.second, post.pub_date.second)
		self.assertEquals(only_post.text, 'This is a test post for testing.')
		self.assertEquals(only_post.slug, 'test-post')

# Base class that the following test classes can inherit from. Thus we don't have to have each test class inherit from LiveServerTestCase
class BaseAcceptanceTest(LiveServerTestCase):
	def set_up(self):
		self.client = Client()

# Test login on the admin page
class AdminTest(BaseAcceptanceTest):

	# Load fixtures
	fixtures = ['users.json']

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
			'pub_date_1': '12:56:05',
			'slug': 'test-post'
			},
			follow = True)
		self.assertEquals(response.status_code, 200)

		# Check added successfully
		self.assertTrue('added successfully' in smart_text(response.content))

		# Check that the post is now in the database
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

	def test_edit_post(self):

		# Create a blog author
		author = User.objects.create_user('TestUser', 'test@user.com', 'password')
		author.save

		# Create the post
		post = Post()
		post.title = 'Test post number 1'
		post.author = author
		post.pub_date = timezone.now()
		post.text = 'This is the first test post for testing.'
		post.slug = 'test-post-number-1'

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
			'pub_date_1': '12:56:05',
			'slug': 'test-post-number-2'
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

		# Create a blog author
		author = User.objects.create_user('TestUser', 'test@user.com', 'password')
		author.save

		# Creates the post
		post = Post()

		# Sets the attributes of the post
		post.title = 'Test post'
		post.author = author
		post.pub_date = timezone.now()
		post.text = 'This is a test post for testing.'
		post.slug = 'test-post'

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
class PostViewTest(BaseAcceptanceTest):

	def test_index(self):
		# Create a blog author
		author = User.objects.create_user('TestUser', 'test@user.com', 'password')
		author.save

		#Create a post
		post = Post()

		# Sets the attributes of the post
		post.title = 'Test post'
		post.author = author
		post.pub_date = timezone.now()
		post.text = 'This is a test [post for testing.](http://127.0.0.1:8000/)'
		post.slug = 'test-post'

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

	def test_post_page(self):

		# Create a blog author
		author = User.objects.create_user('TestUser', 'test@user.com', 'password')
		author.save

		# Create a post
		post = Post()

		# Ammend to post
		post.title = 'Another first post'
		post.author = author
		post.pub_date = timezone.now()
		post.text = 'This is a test post [for a blog.](http://127.0.0.1:8000/)'
		post.slug = 'another-first-post'

		post.save()

		# Confirm that a new post has been saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Get the URL of the post
		post_url = only_post.get_abs_url()

		# Fetch the post
		response = self.client.get(post_url, follow = True)
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
		self.assertTrue('<a href="http://127.0.0.1:8000/">for a blog.</a>' in smart_text(response.content))

# Test for flat pages
class FlatPageViewTest(BaseAcceptanceTest):

	def test_create_flat_page(self):

		# Create a flat page
		page = FlatPage()
		page.url = '/about/'
		page.title = 'Test flat page about me'
		page.content = 'Here is all my information.'

		page.save()

		# Add the site
		page.sites.add(Site.objects.all()[0])
		page.save()

		# Check that the new page is saved
		all_pages = FlatPage.objects.all()
		self.assertEquals(len(all_pages), 1)
		only_page = all_pages[0]
		self.assertEquals(only_page, page)

		# Check that the data is correct
		self.assertEquals(only_page.url, '/about/')
		self.assertEquals(only_page.title, 'Test flat page about me')
		self.assertEquals(only_page.content, 'Here is all my information.')

		# Get the url
		page_url = only_page.get_absolute_url()

		# Get the page
		response = self.client.get(page_url, follow = True)
		self.assertEquals(response.status_code, 200)

		# Check that the title and content is in the response
		self.assertTrue('Test flat page about me' in smart_text(response.content))
		self.assertTrue('Here is all my information.' in smart_text(response.content))
