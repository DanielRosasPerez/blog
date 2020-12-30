from django.db import models

# Create your models here.

from django.utils import timezone
#from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager

class PublishedManager(models.Manager): # Since we are going to create a new manager to retrive all "posts" with the "published" status.

        def get_queryset(self): # This method returns the QuerySet that will be executed.

            # In order to include our custom "filter" in the final "QuerySet", we will override this method.
            return super(PublishedManager,self).get_queryset().filter(status="published") # Here, we are overriding "get_queryset()" method.

class Post(models.Model):

    STATUS_CHOICES = (("draft","Draft"),("published","Published"))
    title = models.CharField(max_length=200) # Field for the POST TITLE.
    slug = models.CharField(max_length=200, unique_for_date="publish") # When using "unique_for_date" Django won't allow the entry of two instances from the same model with the same "slug" and "publish" date.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_post") # We use "ForeignKey" whenever we want to establish a
    # relationship "Many-to-one". On the other hand, "related_name" allow us to name the attribute for the object related to the instance created from this class.
    # "A USER CAN POST MULTIPLE POSTS."
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    #publish = models.DateTimeField(default=datetime.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    #class Meta: # This class contains the METADATA.

    #    ordering = ["-publish",] # We are going to order the posts from the more recent published to the old one.


    def __str__(self): # This magic function (in this case, method), is the default human-redable representation of the object.
        return self.title # In order for any instance created using this model to be named as its respective title.

    def get_absolute_url(self): # We will use this method in our templates to link to specific posts.
        return reverse("users_blog:post_detail", args=[self.publish.year,self.publish.month,self.publish.day,self.slug])

    # The first manager declared in a model becomes the default manager of it.
    # In order to keep the "default manager" inside our model (as a second option), we need to declare this explicitly in the model,
    # otherwise, it will be override and we won't be able to use it.
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    tags = TaggableManager() # This manager will allow us to add, retrieve and remove tags from Post instances/objects.

######################################################################################################################################

class Comment(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments") # We use "ForeignKey" whenever we want a relationship
    # Many-to-one. On the other hand, "related_name" allow us to name the attribute for the object related to the instance created from this class.
    # In this case, we want to associate all the instances from this model with a single post. "A POST CAN HAVE MULTIPLE COMMENTS."
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:

        ordering = ["created",] # To sort comments in a chronological order by default.

        def __str__(self):
            return f"Comment by {self.name} on {self.post}"

    # Note: The relationship "Many-to-one" is defined in the "Comment" model because "each comment will be made on one post, and each post may
    # have multiple comments."

    # Note 2: Since we have defined the relationship "Many-to-one", we can "retrieve the post of a comment instance using 'comment.post'".
    # On the other hand, we can "retrieve all comments of a post instance using post.comments.all()." Notice that the second argument from the 
    # instance "comment" and the instance "post" is the "related_name" declared in the foreign key from the the respective model.

    # Note 3: If we don't define "related_name", by default Django will use the "name of the model in lowercase", followed by "_set" (comment_set),
    # to name the relationship of the releated object to the object of the model.

######################################################################################################################################