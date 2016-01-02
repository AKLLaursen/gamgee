from django.conf.urls import url
from django.views.generic import ListView
from blogengine.models import Post

# Note that patterns has been deprecated since 1.8.

urlPatterns = [
		# Index
		url('^$', ListView.as_view(
			model = Post,
			)),
]