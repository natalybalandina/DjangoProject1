from django.contrib import admin

from blogs.models import BlogPost


# Register your models here.
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "preview_image", "publication_sign", "count_views")
    list_filter = ("publication_sign",)
    search_fields = ("title", "content")
