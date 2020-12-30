"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# URL patterns allow us to map URLs to views.py.
# As we can see from the top wide string, a URL pattern is composed of a "string pattern", a "view" and, optionally (but I use it anyway), 
# a "name" that makes a reference to a specific view.

from django.contrib import admin
from django.urls import path, include

# C:
from django.contrib.sitemaps.views import sitemap
from users_blog.sitemaps import PostSitemap
sitemaps = {"posts":PostSitemap}

# Note: Namespaces have to be "UNIQUE" across our entire projects.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include("users_blog.urls", namespace="users_blog")), # This way, we include the URL patterns from the app "users_blog", and 
    # whenever we want to reference the "urls" from this app, we just need to use the "namespace" followed by a colon (:). For example:
    # "users_blog:post_list" or "users_blog:post_detail".
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps}, name="django.contrib.sitemaps.views.sitemap"), # C.
]

# The code that belongs to "C", we have included the required imports and defined a dictionary of sitemaps. You define an URL pattern that
# matches "sitemap.xml" and uses the "sitemap" view. The "sitemaps" dictionary is passed to the "sitemap" view.