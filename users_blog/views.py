from django.shortcuts import render, get_object_or_404 # "get_object_or_404()" retrieves the desired post. However, if such post doesn't exist
# it will return an HTTP 404 (NOT FOUND) exception.

from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # In order to make the "pagination".

from taggit.models import Tag # Importing the Tag model from the third-party app. By default this models has relationship "Many-to-many".

from django.db.models import Count # This is the count aggregation function of the Django ORM. This function will allow us to perform aggregated
# counts of tags.

# "django.db.models" include the following aggregation functions:
#   Avg: The mean value.
#   Max: The maximum value.
#   Min: The minimum value.
#   Count: The total number of objects.
#  
# We can learn more about aggregation at: https://docs.djangoproject.com/en/3.0/topics/db/aggregation/.

# Create your views here.
"""
# We keep these old views in order to see how they evolve.

def post_list(request): # Since whenever we ask for the view a query is made, so, we need a variable to handle it, that's why we pass "request".
    posts = Post.published.all() # Here, we retrieve all the instances created from "Post" that have their "status" field as "published".
    return render(request, "users_blog/post/list.html", {"posts":posts}) # We use render() shortcut to render the list of posts with the given template.

    # "render()" takes the request object, the template path, and the context variables to render the given template. It returns an
    #  "HTTP response" object with the rendered text (normally HTML code).
"""

def post_list(request, tag_slug=None):
    object_list = Post.published.all() # We retrive all the instances created from "Post" model (every instance is retrieved with all its attributes/fields and methods), that have their "status" as "published". 
    
    # Since this is a "Many-to-many" relationship, we have to filter posts by tags contained in a given list, which in our case contains only
    # one element. This is, we will search for one tag.
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    
    paginator = Paginator(object_list,3) # 3 posts per page.
    page = request.GET.get('page') # We retrieve the current page number.
    try:
        posts = paginator.page(page) # We obtain the objects for the selected page.
    except PageNotAnInteger:
        posts = paginator.page(1) # If page is not an integer deliver, then we obtain the objects from the first page:
    return render(request, "users_blog/post/list.html", {"page":page, "posts":posts, "tag":tag}) # We pass the page number and the retrieved objects to the template.

from django.views.generic import ListView
class PostListView(ListView): # This CBV will allow us to list objects of any kind. This is "GENERIC VIEW".
    queryset = Post.published.all() # Use a specific QuerySet instead of retrieving all objects. Instead of defining a "queryset" attribute,
    # we could have specified "model = Post" and Django would have built the generic "Post.objects.all()" QuerySet for us (this way, all the
    # the objects created from Post would be retrieved).
    context_object_name = "posts" # Use the context variable posts for the query results. The default variable is "object_list" if you don't
    # specify any "context_object_name".
    paginate_by = 3 # Paginate the results, listing 3 posts (also known as objects from Post model), per page.
    template_name = "users_blog/post/list.html" # Use a custom template to render the page. If we don't set a default template, "ListView" will
    # use the template "post_list.html".

    # Note: ListView passes the selected page in a variable called "object_list".

######################################################################################################################################

"""

# We keep these old views in order to see how they evolve.

def post_detail(request, year, month, day, post): # This second view will display a single post.
    post = get_object_or_404(Post, slug=post, status="published", publish__year=year, publish__month=month, publish__day=day)
    return render(request, "users_blog/post/detail.html", {"post":post}) # To render the retrieved SINGLE post using a template.

    # This views takes the "year", "month", "day" and post arguments to retrieve a single published post with the given slug and date.

"""

from .models import Comment
from .forms import CommentForm
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status="published", publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True) # Retrieve a list of active comments for this post.
    new_comment = None # To initialize the variable. We will use this variable when a new comment is created.
    if request.method == "POST": # The form of a comment was filled in and a comment was posted.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False) # Create a new comment instance, but don't save to database yet. This is useful
            # when we want to modify the instance/object before save it into the database.
            new_comment.post = post # Assing the current post to the comment.
            new_comment.save() # Save the comment to the database.
    else: # request.method returns GET. This is, a comment has not been posted yet, so, let's create a new form to make a comment.
            comment_form = CommentForm() # Creating an empty form for a new comment. This is going to be desplayed empyt to post a commment.
    
    # List of similar posts:
    post_tags_ids = post.tags.values_list("id", flat=True) # A.
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id) # B.
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags","-publish")[:4] # C.

    # A. We retrieve a Python list of IDs for the tags of the current post. The "values_list()" QuerySet returns with the values for the 
    # given fields. We pass "flat=True" to it to get single values such as [1,2,3,...] instead of one-tuples such as [(1,), (2,), (3,), ...].

    # B. We get all the posts that contain any of these tags, excluding the current post itself.

    # C. We use the "Count" aggregation function to generate a calculated field (same_tags), that contains the number of tags shared with all
    # the tags queried. Also, we have ordered the results by the number of shared tags (descending order) and by publish to display recent posts
    # first, for the posts with the same number of shared tags. Finally, we have sliced the result to retrieve up to the 4th post.

    return render(request, "users_blog/post/detail.html", {"post":post, "comments":comments, "new_comment":new_comment, 
    "similar_posts":similar_posts,"comment_form":comment_form}) # This combines a given template with a given "context dictionary" and returns
    # an HttpResponse object with that rendered text.

# Note: The "save()" method is available for "ModelForm" but not for "Form" instances, since they are not linked to any model.

######################################################################################################################################
"""
# We keep these old views in order to see how they evolve.

from .forms import EmailPostForm
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published") # Retrieve a post by an id and a published status. If not found, we get a 404 not found page.
    if request.method == "POST": # If the data inside the form (By this we mean the TABLE created by Django not an instance from "EmailPostForm()" yet), 
        # was submitted.
        form = EmailPostForm(request.POST) # "We create an instance from this class" using the data contained in "request.POST".
        if form.is_valid(): # If form field passes validation. "is_valid()" method validates the submitted data for every field
            # and returns "True" if the data for every field inside the form passes. If any field has invalid data, it will return "False".
            cd = form.cleaned_data # We retrieve the validated data. This attribute is a dictionary of form fields and their values.
            # This is, {"field_1":value_1, "field_2":value_2, ...}.
    else:
        form = EmailPostForm() # If we get "GET" instead of a "POST" request, we display an empty form instace for the user to fill in.
    return render(request, "users_blog/post/share.html", {"post":post, "form":form})

    # Note: If "form.is_valid()" is False, the "form" instance will be generated again with the submitted data.

"""
from .forms import EmailPostForm
from django.core.mail import send_mail
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published") # Retrieve a post by an id and a published status. If not found, we get a 404 not found page.
    sent = False
    if request.method == "POST": # If the data inside the form (By this we mean the TABLE created by Django not an instance from "EmailPostForm()" yet), 
        # was submitted.
        form = EmailPostForm(request.POST) # "We create an instance from this class" using the data contained in "request.POST".
        if form.is_valid(): # If form field passes validation. "is_valid()" method validates the submitted data for every field
            # and returns "True" if the data for every field inside the form passes. If any field has invalid data, it will return "False".
            cd = form.cleaned_data # We retrieve the validated data. This attribute is a dictionary of form fields and their values.
            # This is, {"field_1":value_1, "field_2":value_2, ...}.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, "xxxxxx@gmail.com", [cd["to"]]) # Add the same email that you added in "settings.py".
            sent = True
    else:
        form = EmailPostForm() # If we get "GET" instead of a "POST" request, we display an empty form instace for the user to fill in.
    return render(request, "users_blog/post/share.html", {"post":post, "form":form, "sent":sent})

    # Note: If "form.is_valid()" is False, the "form" instance will be generated again with the submitted data.
