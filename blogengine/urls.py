from django.conf.urls import url
from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed
from blogengine.models import Category, Tag, Post
from blogengine.views import CategoryListView, TagListView, PostsFeed

# Note that patterns has been deprecated since 1.8.

urlpatterns = [
		# Index
		url('^(?P<page>\d+)?/?$', ListView.as_view(
			model = Post, paginate_by = 5,
			)),

		# Individual posts
		url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<pub_date__day>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view(model = Post,
			)),

		# Categories
		url(r'^category/(?P<slug>[a-zA-Z0-9-]+)/?$', CategoryListView.as_view(
			paginate_by = 5,
			model = Category,
			)),

		# Tags
		url(r'^tag/(?P<slug>[a-zA-Z0-9-]+)/?$', TagListView.as_view(
			paginate_by = 5,
			model = Tag,
			)),

		# Post RSS feed
		url(r'^feeds/posts/$', PostsFeed()),

]
