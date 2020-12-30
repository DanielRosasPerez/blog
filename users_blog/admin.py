from django.contrib import admin

# Register your models here.

# FIRST MODEL:

from .models import Post

@admin.register(Post) # This decorator makes the same function as "admin.site.register()" function.
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated") # We show the columns "created" and "updated" as readonly fields.
    list_display = ("title", "slug", "author", "publish", "status") # This way, we show these columns in the model (table) Post(s).
    list_filter = ("status", "created", "publish", "author") # This will allow us to filter the results by the fields specified here.
    search_fields = ("title", "body") # This allow us to deploy a search bar and search data by "title" and "body". Try not to use ForeignKey as field for searching, maybe it won't work.
    prepopulated_fields = {"slug":("title",)} # Django is going to fill automatically the field "slug" with the input/text of the title.
    raw_id_fields = ("author",) # When creating an instance of the model and clicking the "author" field, a lookup widget is going to pop up and we should select the "author's USERNAME". It will be saved using its respective id.
    date_hierarchy = "publish" # We deploy some buttons below the search bar to search for data by date hierarchy.
    ordering = ("status", "publish") # The data is orderer first by status and then by publish.

# admin.site.register(Post, PostAdmin) # This function registers our model on the admin site.

# SECOND MODEL:

from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")
    list_display = ("name", "email", "post", "created", "active")
    list_filter = ("active", "created", "updated")
    search_fields = ("name", "email", "body")