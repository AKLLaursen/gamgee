import markdown2 as markdown
import feedparser

from django.test import TestCase, Client, LiveServerTestCase
from django.utils import timezone
from django.utils.encoding import smart_text 
from blogengine.models import Post, Category, Tag
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

# Base class that the following test classes can inherit from. Thus we don't have to have each test class inherit from LiveServerTestCase
class BaseAcceptanceTest(LiveServerTestCase):
	def setUp(self):
		self.client = Client()

# Test for blogpost creation
class PostTest(TestCase):

	def test_create_category(self):

		# Create the category
		category = Category()

		# Add attributes
		category.name = 'Data Science - Test'
		category.description = 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.'
		category.slug = 'data-science-test'

		# Save the category
		category.save()

		# Check that the category can be found
		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 1)
		only_category = all_categories[0]
		self.assertEquals(only_category, category)

		# Checks the attributes of the category
		self.assertEquals(only_category.name, 'Data Science - Test')
		self.assertEquals(only_category.description, 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.')
		self.assertEquals(only_category.slug, 'data-science-test')
		self.assertEquals(only_category.__unicode__(), 'Data Science - Test')

	def test_create_tag(self):

		# Create the tag
		tag = Tag()

		# Add attributes
		tag.name = 'R'
		tag.description = 'The R programming language'
		tag.slug = 'r'

		# Save the tag

		tag.save()

		# Check that the tag can be found
		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 1)
		only_tag = all_tags[0]
		self.assertEquals(only_tag, tag)

		# Check the attributes of the tag
		self.assertEquals(only_tag.name, 'R')
		self.assertEquals(only_tag.description, 'The R programming language')
		self.assertEquals(only_tag.slug, 'r')
		self.assertEquals(only_tag.__unicode__(), 'R')

	def test_create_post(self):

		# Create a category
		category = Category()
		category.name = 'Data Science - Test'
		category.description = 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.'

		category.save()

		# Create the tag
		tag = Tag()
		tag.name = 'R'
		tag.description = 'The R programming language'
		tag.save()

		# Create a blog author
		author = User.objects.create_user('TestUser', 'test@user.com', 'password')
		author.save()

		# Creates the post
		post = Post()

		# Sets the attributes of the post
		post.title = 'Test post'
		post.author = author
		post.pub_date = timezone.now()
		post.category = category
		post.text = 'This is a test post for testing.'
		post.slug = 'test-post'

		# Saves the post
		post.save()

		# Add the tag
		post.tags.add(tag)
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
		self.assertEquals(only_post.category.name, 'Data Science - Test')
		self.assertEquals(only_post.category.description, 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.')
		self.assertEquals(only_post.text, 'This is a test post for testing.')
		self.assertEquals(only_post.slug, 'test-post')
		self.assertEquals(only_post.__unicode__(), 'Test post')

		# Check tags
		post_tags = only_post.tags.all()
		self.assertEquals(len(post_tags), 1)
		only_post_tag = post_tags[0]
		self.assertEquals(only_post_tag, tag)
		self.assertEquals(only_post_tag.name, 'R')
		self.assertEquals(only_post_tag.description, 'The R programming language')

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

	def test_create_category(self):

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Check the response code
		response = self.client.get('/admin/blogengine/category/add/')
		self.assertEquals(response.status_code, 200)

		# Create the new category
		response = self.client.post('/admin/blogengine/category/add/', {
			'name': 'Data Science - Test',
			'description': 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.'
			},
			follow = True
			)
		self.assertEquals(response.status_code, 200)

		# Check that the category is added successfully
		self.assertTrue('added successfully' in smart_text(response.content))

		# Check that the new category is now in the database
		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 1)

	def test_edit_category(self):

		# Create the category
		category = Category()
		category.name = 'Data Science - Test'
		category.description = 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.'

		category.save()

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Get the ID of the category, as this is subject to change
		all_categories = Category.objects.all()
		category_id = all_categories[0].id

		# Edit the category
		response = self.client.post('/admin/blogengine/category/' + str(category_id) + '/change/', {
			'name': 'R',
			'description': 'The R programming language'
			},
			follow = True)
		self.assertEquals(response.status_code, 200)

		# Check that the category is changed successfully
		self.assertTrue('changed successfully' in smart_text(response.content))

		# Check that the category is amended
		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 1)
		only_category = all_categories[0]
		self.assertEquals(only_category.name, 'R')
		self.assertEquals(only_category.description, 'The R programming language')

	def test_delete_category(self):

		# Create the category
		category = Category()
		category.name = 'Data Science - Test'
		category.description = 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.'

		category.save()

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Get the ID of the category, as this is subject to change
		all_categories = Category.objects.all()
		category_id = all_categories[0].id

		# Delete the category
		response = self.client.post('/admin/blogengine/category/' + str(category_id) + '/delete/', {
			'post': 'yes'
			}, follow=True)
		self.assertEquals(response.status_code, 200)

		# Check that the category is deleted successfully
		self.assertTrue('deleted successfully' in smart_text(response.content))

		# Check that the category is deleted
		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 0)

	def test_create_tag(self):

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Check the response code
		response = self.client.get('/admin/blogengine/tag/add/', follow = True)
		self.assertEquals(response.status_code, 200)

		# Create the new tag
		response = self.client.post('/admin/blogengine/tag/add/', {
			'name': 'R',
			'description': 'The R programming language'
			},
			follow = True
			)
		self.assertEquals(response.status_code, 200)

		# Check that the tag was added successfully
		self.assertTrue('added successfully' in smart_text(response.content))

		# Check that the new tag is now in the database
		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 1)

	def test_edit_tag(self):

		# Create the tag
		tag = Tag()
		tag.name = 'R'
		tag.description = 'The Python programming language'

		tag.save()

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Get the ID of the tag, as this is subject to change
		all_tags = Tag.objects.all()
		tag_id = all_tags[0].id

		# Edit the tag
		response = self.client.post('/admin/blogengine/tag/' + str(tag_id) + '/change/', {
			'name': 'Python',
			'description': 'The Python programming language'
			}, follow = True)
		self.assertEquals(response.status_code, 200)

		# Check that the tag has changed successfully
		self.assertTrue('changed successfully' in smart_text(response.content))

		# Check that the tag is amended
		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 1)
		only_tag = all_tags[0]
		self.assertEquals(only_tag.name, 'Python')
		self.assertEquals(only_tag.description, 'The Python programming language')

	def test_delete_tag(self):

		# Create the tag
		tag = Tag()
		tag.name = 'R'
		tag.description = 'The R programming language'

		tag.save()

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Get the ID of the tag, as this is subject to change
		all_tags = Tag.objects.all()
		tag_id = all_tags[0].id

		# Delete the tag
		response = self.client.post('/admin/blogengine/tag/' + str(tag_id) + '/delete/', {
			'post': 'yes'
			}, follow = True)
		self.assertEquals(response.status_code, 200)

		# Check that the tag was deleted successfully
		self.assertTrue('deleted successfully' in smart_text(response.content))

		# Check that the tag is deleted
		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 0)

	def test_create_post(self):

		# Create the category
		category = Category()
		category.name = 'Data Science - Test'
		category.description = 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.'

		category.save()

		# Create the tag
		tag = Tag()
		tag.name = 'R'
		tag.description = 'The R programming language'

		tag.save()

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Check the response code
		response = self.client.get('/admin/blogengine/post/add/', follow = True)
		self.assertEquals(response.status_code, 200)

		# Get the category ID
		all_categories = Category.objects.all()
		category_id = all_categories[0].id

		# Get the tag ID
		all_tags = Tag.objects.all()
		tag_id = all_tags[0].id

		# Create a test post
		response = self.client.post('/admin/blogengine/post/add/', {
			'title': 'Test post',
			'text': 'This is a test post for testing.',
			'pub_date_0': '2015-12-30',
			'pub_date_1': '12:56:05',
			'slug': 'test-post',
			'category': str(category_id),
			'tags': str(tag_id)
			},
			follow = True)
		self.assertEquals(response.status_code, 200)

		# Check added successfully
		self.assertTrue('added successfully' in smart_text(response.content))

		# Check that the post is now in the database
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

	def test_edit_post(self):

		# Create the category
		category = Category()
		category.name = 'Data Science - Test'
		category.description = 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.'

		category.save()

		# Create the tag
		tag = Tag()
		tag.name = 'R'
		tag.description = 'The R programming language'

		tag.save()

		# Create a blog author
		author = User.objects.create_user('TestUser', 'test@user.com', 'password')

		author.save()

		# Create the post
		post = Post()
		post.title = 'Test post number 1'
		post.author = author
		post.pub_date = timezone.now()
		post.text = 'This is the first test post for testing.'
		post.slug = 'test-post-number-1'

		post.save()

		post.tags.add(tag)
		post.save()

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Get the ID of the post, as this is subject to change
		all_posts = Post.objects.all()
		post_id = all_posts[0].id

		# Get the category ID
		all_categories = Category.objects.all()
		category_id = all_categories[0].id

		# Get the tag ID
		all_tags = Tag.objects.all()
		tag_id = all_tags[0].id

		# Edit the post
		response = self.client.post(('/admin/blogengine/post/' + str(post_id) + '/change/'), {
			'title': 'Test post number 2',
			'text': 'This is the second test post for testing.',
			'pub_date_0': '2015-12-30',
			'pub_date_1': '12:56:05',
			'slug': 'test-post-number-2',
			'category': str(category_id),
			'tags': str(tag_id)
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

		# Create the category
		category = Category()
		category.name = 'Data Science - Test'
		category.description = 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.'

		category.save()

		# Create the tag
		tag = Tag()
		tag.name = 'R'
		tag.description = 'The R programming language'

		tag.save()

		# Create a blog author
		author = User.objects.create_user('TestUser', 'test@user.com', 'password')

		author.save()

		# Creates the post
		post = Post()

		# Sets the attributes of the post
		post.title = 'Test post'
		post.author = author
		post.category = category
		post.pub_date = timezone.now()
		post.text = 'This is a test post for testing.'
		post.slug = 'test-post'

		post.save()

		post.tags.add(tag)
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

	def test_create_post_without_tag(self):

		# Create the category
		category = Category()
		category.name = 'Data Science - Test'
		category.description = 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.'

		category.save()

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Check the response code
		response = self.client.get('/admin/blogengine/post/add/')
		self.assertEquals(response.status_code, 200)

		# Get the category ID
		all_categories = Category.objects.all()
		category_id = all_categories[0].id

		# Create the new post
		response = self.client.post('/admin/blogengine/post/add/', {
			'title': 'This is another test post',
			'text': 'This is the text',
			'pub_date_0': '2016-01-17',
			'pub_date_1': '15:05:00',
			'slug': 'my-first-post',
			'category': str(category_id)
			},
			follow = True
			)
		self.assertEquals(response.status_code, 200)

		# Check added successfully
		self.assertTrue('added successfully' in smart_text(response.content))

		# Check new post now in database
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

	def test_create_post_without_categorys(self):

		# Create the tag
		tag = Tag()
		tag.name = 'R'
		tag.description = 'The R programming language'

		tag.save()

		# Log in
		self.client.login(username = 'testuser', password = 'testuserpass')

		# Check the response code
		response = self.client.get('/admin/blogengine/post/add/')
		self.assertEquals(response.status_code, 200)

		# Get the tag ID
		all_tags = Tag.objects.all()
		tag_id = all_tags[0].id

		# Create the new post
		response = self.client.post('/admin/blogengine/post/add/', {
			'title': 'This is another test post',
			'text': 'This is the text',
			'pub_date_0': '2016-01-17',
			'pub_date_1': '15:05:00',
			'slug': 'my-first-post',
			'tag': str(tag_id)
			},
			follow = True
			)
		self.assertEquals(response.status_code, 200)

		# Check added successfully
		self.assertTrue('added successfully' in smart_text(response.content))

		# Check new post now in database
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

# Test for Views
class PostViewTest(BaseAcceptanceTest):

	def test_index(self):

		# Create the category
		category = Category()
		category.name = 'Data Science - Test'
		category.description = 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.'

		category.save()

		# Create the tag
		tag = Tag()
		tag.name = 'R'
		tag.description = 'The R programming language'

		tag.save()

		# Create a blog author
		author = User.objects.create_user('TestUser', 'test@user.com', 'password')

		author.save()

		#Create a post
		post = Post()

		# Sets the attributes of the post
		post.title = 'Test post'
		post.author = author
		post.category = category
		post.pub_date = timezone.now()
		post.text = 'This is a test [post for testing.](http://127.0.0.1:8000/)'
		post.slug = 'test-post'

		post.save()

		post.tags.add(tag)
		post.save()

		# Check that a new post is saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

		# Get the index
		response = self.client.get('/', follow = True)
		self.assertEquals(response.status_code, 200)

		# Check that the post title is in the reponse
		self.assertTrue(post.title in smart_text(response.content))

		# Check the post category is in the response
		self.assertTrue(post.category.name in smart_text(response.content))

		# Check the post tag is in the response
		post_tag = all_posts[0].tags.all()[0]
		self.assertTrue(post_tag.name in smart_text(response.content))

		# Check that the post text is in the response
		self.assertTrue(markdown.markdown(post.text) in smart_text(response.content))

		# Check that the post date is in the response
		self.assertTrue(str(post.pub_date.year) in smart_text(response.content))
		self.assertTrue(post.pub_date.strftime('%b') in smart_text(response.content))
		self.assertTrue(str(post.pub_date.day) in smart_text(response.content))

		# Check the link is marked up properly
		self.assertTrue('<a href="http://127.0.0.1:8000/">post for testing.</a>' in smart_text(response.content))

	def test_post_page(self):

		# Create the category
		category = Category()
		category.name = 'Data Science - Test'
		category.description = 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.'

		category.save()

		# Create the tag
		tag = Tag()
		tag.name = 'R'
		tag.description = 'The R programming language'

		tag.save()

		# Create a blog author
		author = User.objects.create_user('TestUser', 'test@user.com', 'password')

		author.save()

		# Create a post
		post = Post()

		# Ammend to post
		post.title = 'Another first post'
		post.author = author
		post.category = category
		post.pub_date = timezone.now()
		post.text = 'This is a test post [for a blog.](http://127.0.0.1:8000/)'
		post.slug = 'another-first-post'

		post.save()

		post.tags.add(tag)
		post.save()

		# Confirm that a new post has been saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Get the URL of the post
		post_url = only_post.get_absolute_url()

		# Fetch the post
		response = self.client.get(post_url, follow = True)
		self.assertEquals(response.status_code, 200)

		# Check that the post title is in the reponse
		self.assertTrue(post.title in smart_text(response.content))

		# Check that the post text is in the response
		self.assertTrue(markdown.markdown(post.text) in smart_text(response.content))

		# Check the post category is in the response
		self.assertTrue(post.category.name in smart_text(response.content))

		# Check the post tag is in the response
		post_tag = all_posts[0].tags.all()[0]
		self.assertTrue(post_tag.name in smart_text(response.content))

		# Check that the post date is in the response
		self.assertTrue(str(post.pub_date.year) in smart_text(response.content))
		self.assertTrue(post.pub_date.strftime('%b') in smart_text(response.content))
		self.assertTrue(str(post.pub_date.day) in smart_text(response.content))

		# Check the link is marked up properly
		self.assertTrue('<a href="http://127.0.0.1:8000/">for a blog.</a>' in smart_text(response.content))

	def test_category_page(self):

		# Create the category
		category = Category()
		category.name = 'Data Science - Test'
		category.description = 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.'

		category.save()

		# Create a blog author
		author = User.objects.create_user('TestUser', 'test@user.com', 'password')

		author.save()

		# Create a post
		post = Post()

		# Ammend to post
		post.title = 'Another first post'
		post.author = author
		post.category = category
		post.pub_date = timezone.now()
		post.text = 'This is a test post [for a blog.](http://127.0.0.1:8000/)'
		post.slug = 'another-first-post'

		post.save()

		# Confirm that a new post has been saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Get the category URL
		category_url = post.category.get_absolute_url()

		# Fetch the category
		response = self.client.get(category_url, follow = True)
		self.assertEquals(response.status_code, 200)

		# Check that the categeory name is in the reponse
		self.assertTrue(category.name in smart_text(response.content))

		# Check that the post text is in the response
		self.assertTrue(markdown.markdown(post.text) in smart_text(response.content))

		# Check that the post text is in the response
		self.assertTrue(markdown.markdown(post.text) in smart_text(response.content))

		# Check that the post date is in the response
		self.assertTrue(str(post.pub_date.year) in smart_text(response.content))
		self.assertTrue(post.pub_date.strftime('%b') in smart_text(response.content))
		self.assertTrue(str(post.pub_date.day) in smart_text(response.content))

		# Check the link is marked up properly
		self.assertTrue('<a href="http://127.0.0.1:8000/">for a blog.</a>' in smart_text(response.content))

	def test_tag_page(self):

		# Create the tag
		tag = Tag()
		tag.name = 'R'
		tag.description = 'The R programming language'

		tag.save()

		# Create a blog author
		author = User.objects.create_user('TestUser', 'test@user.com', 'password')

		author.save()

		# Create the post
		post = Post()

		# Ammend to post
		post.title = 'Another first post'
		post.author = author
		post.pub_date = timezone.now()
		post.text = 'This is a test post [for a blog.](http://127.0.0.1:8000/)'
		post.slug = 'another-first-post'

		post.save()

		post.tags.add(tag)
		post.save()

		# Check new post saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Get the tag URL
		tag_url = post.tags.all()[0].get_absolute_url()

		# Fetch the tag
		response = self.client.get(tag_url, follow = True)
		self.assertEquals(response.status_code, 200)

		# Check the tag name is in the response
		self.assertTrue(post.tags.all()[0].name in smart_text(response.content))

		# Check the post text is in the response
		self.assertTrue(markdown.markdown(post.text) in smart_text(response.content))

		# Check the post date is in the response
		self.assertTrue(str(post.pub_date.year) in smart_text(response.content))
		self.assertTrue(post.pub_date.strftime('%b') in smart_text(response.content))
		self.assertTrue(str(post.pub_date.day) in smart_text(response.content))

		# Check the link is marked up properly
		self.assertTrue('<a href="http://127.0.0.1:8000/">for a blog.</a>' in smart_text(response.content))

	def test_nonexistent_category_page(self):

		category_url = '/category/blah/'

		response = self.client.get(category_url, follow = True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('No posts found' in smart_text(response.content))

	def test_nonexistent_tag_page(self):

		tag_url = '/tag/blah/'

		response = self.client.get(tag_url, follow = True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('No posts found' in smart_text(response.content))

	def test_clear_cache(self):

		# Create the category

		category = Category()
		category.name = 'R'
		category.description = 'The R programming language'

		category.save()

		# Create the tag
		tag = Tag()
		tag.name = 'Python'
		tag.description = 'The Python programming language'

		tag.save()

		# Create the author
		author = User.objects.create_user('TestUser', 'test@user.com', 'password')

		author.save()

		# Create the first post
		post = Post()
		post.title = 'This is a test post'
		post.text = 'Look at this testing of [my first blog post](http://127.0.0.1:8000/)'
		post.slug = 'this-is-a-test-post'
		post.pub_date = timezone.now()
		post.author = author
		post.category = category

		post.save()

		post.tags.add(tag)

		post.save()

		# Check new post saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

		# Fetch the index
		response = self.client.get('/', follow = True)
		self.assertEquals(response.status_code, 200)

		# Create the second post
		post = Post()
		post.title = 'A second test post'
		post.text = 'Look at this testing of [my second blog post](http://127.0.0.1:8000/)'
		post.slug = 'a-second-test-post'
		post.pub_date = timezone.now()
		post.author = author
		post.category = category

		post.save()

		post.tags.add(tag)

		post.save()

		# Fetch the index again
		response = self.client.get('/', follow = True)

		# Check second post present
		self.assertTrue('my second blog post' in smart_text(response.content))

class FeedTest(BaseAcceptanceTest):

	def test_all_post_feed(self):

		# Create the category
		category = Category()
		category.name = 'Data Science - Test'
		category.description = 'Test: Data Science is an interdisciplinary field about processes and systems to extract knowledge or insights from data in various forms.'

		category.save()

		# Create the tag
		tag = Tag()
		tag.name = 'R'
		tag.description = 'The R programming language'

		tag.save()

		# Create a blog author
		author = User.objects.create_user('TestUser', 'test@user.com', 'password')

		author.save()

		# Create a post
		post = Post()

		# Ammend to post
		post.title = 'Another first post'
		post.author = author
		post.category = category
		post.pub_date = timezone.now()
		post.text = 'This is a test post [for a blog.](http://127.0.0.1:8000/)'
		post.slug = 'another-first-post'

		post.save()

		post.tags.add(tag)
		post.save()

		# Check we can find it
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Fetch the feed
		response = self.client.get('/feeds/posts/', follow = True)
		self.assertEquals(response.status_code, 200)

		# Parse the feed
		feed = feedparser.parse(smart_text(response.content))

		# Check length
		self.assertEquals(len(feed.entries), 1)

		# Check post retrieved is the correct one
		feed_post = feed.entries[0]
		self.assertEquals(feed_post.title, post.title)
		self.assertEquals(feed_post.description, post.text)

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
