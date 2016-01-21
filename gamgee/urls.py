from django.conf.urls import url, include
from django.contrib import admin

# Note, no need to add admin.autodiscover() since 1.7. Note also that patterns has been deprecated since 1.8.

urlpatterns = [
    # Admin URLs
    url(r'^admin/', admin.site.urls),

    # Blogengine URLs
    url(r'', include('blogengine.urls', namespace = 'blogengine')),

    # Flat page ULs
    url(r'', include('django.contrib.flatpages.urls')),
]
