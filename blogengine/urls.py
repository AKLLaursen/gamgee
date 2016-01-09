from django.conf.urls import url
from django.views.generic import ListView, DetailView
from blogengine.models import Post

# Note that patterns has been deprecated since 1.8.

urlpatterns = [
		# Index
		url('^(?P<page>\d+)?/?$', ListView.as_view(
			model = Post, paginate_by = 5,
			)),

		# Individual posts
		url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<pub_date__day>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view(model = Post,
			)),
]