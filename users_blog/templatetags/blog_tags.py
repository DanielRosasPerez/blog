from django import template
from ..models import Post

register = template.Library() # Creating an instance to register our custom template tags.

# Custom Template tag 1:

# To obtain the total number of posts with their status as published:
@register.simple_tag
def total_posts(): # Template tag.
    return Post.published.count()

# Custom Template tag 2:

# To display the latest posts in the sidebar of our blog:
@register.inclusion_tag("users_blog/post/latest_posts.html") # An "inclusion_tag" allow us to render a template with context variables returned
# by our template tag.
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts":latest_posts}

# Custom Template tag 3:

from django.db.models import Count
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count("comments")).order_by("-total_comments")[:count]

# The "annotate()" function relates whatever we declare inside its parentheses with every instance created from the model. So, in our case,
# we use "annotate()" to relate the number of comments with its respective post. This is, we obtain the total number of comments per post (since
# we are using the "Count" aggregation function). We store the total number of comments in the variable "total_comments" and we use this variable
# to order the results.

# Custom Template filter 1:

from django.utils.safestring import mark_safe
import markdown # This module allows us to convert the contents from a post to HTML in the templates.
@register.filter(name="markdown") # We give an alias to the filter. The alias (in this case), is "markdown"
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

# To prevent a name clash between our function name and the "markdown" module, we name our function "markdown_format" and name the filter
# "markdown" for use in templates. Once in templates we declare this custom filter as: {{ <variable>|markdown }}.

# Using this module (markdown), we can convert the HTML entities to HTML encode characaters. For example: "<p>" will be "&lt;p&gt;" (less than
# symbol, p character, greater than symbol). We use the "mark_safe" function provided by Django to mark the result as safe HTML to be rendered
# in the template.

# Note: BY DEFAULT, DJANGO WILL NOT TRUST ANY HTML CODE and will escape it before placing it in the output. THE ONLY EXCEPTIONS ARE VARIABLES
# THAT ARE MARKED AS SAFE FROM ESCAPING.
