import markdown2

from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib.syndication.views import Feed
from blogengine.models import Category, Tag, Post
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text

class CategoryListView(ListView):

	template_name = 'blogengine/category_post_list.html'

	def get_queryset(self):
		slug = self.kwargs['slug']

		try:
			category = Category.objects.get(slug = slug)
			return Post.objects.filter(category = category)
			
		except Category.DoesNotExist:
			return Post.objects.none()

	def get_context_data(self, **kwargs):

		context = super(CategoryListView, self).get_context_data( **kwargs)
		slug = self.kwargs['slug']

		try:
			context['category'] = Category.objects.get(slug = slug)

		except Category.DoesNotExist:
			context['category'] = None
		
		return context

class TagListView(ListView):

	template_name = 'blogengine/tag_post_list.html'

	def get_queryset(self):
		slug = self.kwargs['slug']

		try:
			tag = Tag.objects.get(slug = slug)
			return tag.post_set.all()

		except Tag.DoesNotExist:
			return Post.objects.none()

	def get_context_data(self, **kwargs):

		context = super(TagListView, self).get_context_data(**kwargs)
		slug = self.kwargs['slug']

		try:
			context['tag'] = Tag.objects.get(slug = slug)
		except Tag.DoesNotExist:
			context['tag'] = None

		return context

class PostsFeed(Feed):

	title = 'RSS feed - posts'
	link = 'feeds/posts/'
	description = 'RSS feed - blog posts'

	def items(self):
		return Post.objects.order_by('-pub_date')

	def item_title(self, item):
		return item.title

	def item_description(self, item):

		extras = ['fenced-code-blocks']

		content = mark_safe(markdown2.markdown(force_text(item.text), extras = extras))

		return content

class CategoryPostsFeed(PostsFeed):

	def get_object(self, request, slug):
		return get_object_or_404(Category, slug = slug)

	def title(self, obj):
		return 'RSS feed - blog posts in category {0}'.format(str(obj.name))

	def link(self, obj):
		return obj.get_absolute_url()

	def description(self, obj):
		return 'RSS feed - blog posts in category {0}'.format(str(obj.name))

	def items(self, obj):
		return Post.objects.filter(category = obj).order_by('-pub_date')

class TagPostsFeed(PostsFeed):

	def get_object(self, request, slug):
		return get_object_or_404(Tag, slug = slug)

	def title(self, obj):
		return 'RSS feed - blog posts tagged  {0}'.format(obj.name)

	def link(self, obj):
		return obj.get_absolute_url()

	def description(self, obj):
		return 'RSS feed - blog posts tagged {0}'.format(obj.name)

	def items(self, obj):

		try:
			tag = Tag.objects.get(slug = obj.slug)
			return tag.post_set.all()

		except Tag.DoesNotExist:
			return Post.objects.none()
