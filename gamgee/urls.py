from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    # Admin URLs
    url(r'^admin/', admin.site.urls),

    # Blogengine URLs
    url(r'', include('blogengine.urls')),

    # Flat page ULs
    url(r'', include('django.contrib.flatpages.urls')),
]
