from django.conf.urls import url
from django.views.generic import ListView, DetailView
from django.views.generic.dates import ArchiveIndexView
from blogengine.models import Category, Tag, Post
from blogengine.views import CategoryListView, TagListView, PostMonthArchiveView, PostsFeed, CategoryPostsFeed, TagPostsFeed, getSearchResults
from django.contrib.sitemaps.views import sitemap
from blogengine.sitemap import PostSitemap, FlatpageSitemap

# Define appname
app_name = 'blogengine'

# Define sitemaps
sitemaps = {
	'posts': PostSitemap,
	'pages': FlatpageSitemap
}

# Note that patterns has been deprecated since 1.8.

urlpatterns = [
		# Index
		url('^(?P<page>\d+)?/?$', ListView.as_view(
			model = Post, paginate_by = 5,
			), name = 'index'),

		# Individual posts
		url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<pub_date__day>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view(model = Post,
			), name = 'post'),

		# Categories
		url(r'^category/(?P<slug>[a-zA-Z0-9-]+)/?$', CategoryListView.as_view(paginate_by = 5, model = Category,
			), name = 'category'),

		# Tags
		url(r'^tag/(?P<slug>[a-zA-Z0-9-]+)/?$', TagListView.as_view(
			paginate_by = 5, model = Tag,
			), name = 'tag'),

		# Post RSS feed
		url(r'^feeds/posts/$', PostsFeed()),

		# Category RSS feed
    url(r'^feeds/posts/category/(?P<slug>[a-zA-Z0-9-]+)/?$', CategoryPostsFeed()),

    # Tag RSS feed
    url(r'^feeds/posts/tag/(?P<slug>[a-zA-Z0-9-]+)/?$', TagPostsFeed()),

    # Search posts
    url(r'^search', getSearchResults, name = 'search'),

    # Sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name = 'django.contrib.sitemaps.views.sitemap'),

    # Archive
    url(r'^archive/$', ArchiveIndexView.as_view(model = Post, date_field = "pub_date"),
    	name = "post_archive"),

    # Month archive
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
    	PostMonthArchiveView.as_view(month_format = '%m'),
    	name = "post_archive_month"),

]
