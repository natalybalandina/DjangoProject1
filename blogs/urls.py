from blogs.apps import BlogsConfig
from django.urls import path

from blogs.views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
)

app_name = BlogsConfig.name


urlpatterns = [
    path("", BlogPostListView.as_view(), name="blog_list"),
    path("blog_detail/<int:pk>/", BlogPostDetailView.as_view(), name="blog_detail"),
    path("create/", BlogPostCreateView.as_view(), name="blog_create"),
    path("update/<int:pk>/", BlogPostUpdateView.as_view(), name="blog_update"),
    path("delete/<int:pk>/", BlogPostDeleteView.as_view(), name="blog_delete"),
]