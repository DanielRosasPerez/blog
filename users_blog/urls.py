
# A URL pattern is composed of a "string pattern", a "view" and a "name" (the name references an specific view).

from django.urls import path
from . import views

app_name = "users_blog" # Defining a namespace application. This allows us to organize URLs by app and use the name when referring to them.
# This is useful when every app has its own "urls.py" file. It means that we are going to use "include(<app_name>.urls)" in the main "urls.py"
# file. "app_name" is not a must, it is just a wildcard (comodín).

urlpatterns = [
    path('', views.post_list, name="post_list"), # This URLpattern doesn't take any arguments. It is directly mapped to the "post_list" view.
    path('tag/<slug:tag_slug>/', views.post_list, name="post_list_by_tag"),
    #path('', views.PostListView.as_view(), name="PostListView"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name="post_detail"), # The same goes for this view. However, this
    # pattern does have arguments.
    path('<int:post_id>/share/', views.post_share, name="post_share"),
]

# The "url" for the second path will go something like this: <server>/blog/tag/<tag_slug>/
# For example (for music tag): http://127.0.0.1:8000/blog/tag/music/

# Note: The first two paths points to the same view (post_list). Nevertheless, the first one doesn't require any additional argument. On the
#       other hand, the second one ask you for the "tag_slug" argument. We can see what kind of result return to us this view by
#       going into "views.py" and look for "post_list".

# Note 2: We use path "slug" to convert the parameter as a lowercase string with ASCII letters or numbers, plus the hyphen and underscore 
#         character.
