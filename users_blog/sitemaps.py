from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.9 # Max value is 1.

    def items(self): # This returns the QuerySet of objects to include in this sitemap. By default, Django calls "get_absolute_url()" method on
        # each object to retrieve its URL.
        return Post.published.all()

    def lastmod(self, obj): # This method receives each object returned by "items()" and returns the last time the object was modified.
        return obj.updated

# We have create a "sitemap" by inheriting the Sitemap class. The "changefreq" and "priority" attributes indicate the change frequency of our
# post pages and their relevance in our website.

# Note: Both, "changefreq" and "priority" can be either methods or attributes.