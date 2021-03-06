from django.contrib import admin
from .models import Category, Tag, Post
from django.contrib.auth.models import User

class PostAdmin(admin.ModelAdmin):
	
	prepopulated_fields = {'slug': ('title',)}
	exclude = ('author',)

	def save_model(self, request, obj, form, change):
		obj.author = request.user
		obj.save()

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)