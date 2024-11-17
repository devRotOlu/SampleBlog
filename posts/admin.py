from django.contrib import admin

from .models import Post

# Register your models here.

# customizes the Post admin.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=["title","created"]
    list_filter=['created']