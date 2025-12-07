from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from blogs.forms import BlogPostForm
from blogs.models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blogs/blog_list.html"
    context_object_name = "blog_posts"

    def get_queryset(self):
        return BlogPost.objects.filter(publication_sign=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blogs/blog_detail.html"
    context_object_name = "blog_post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.count_views += 1
        obj.save(update_fields=["count_views"])  # Сохраняет только поле count_views
        return obj


class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = "blogs/blog_create.html"
    form_class = BlogPostForm
    success_url = reverse_lazy("blogs:blog_list")


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = "blogs/blog_create.html"
    form_class = BlogPostForm
    success_url = reverse_lazy("blogs:blog_list")

    def get_success_url(self):
        return reverse("blogs:blog_detail", args=[self.kwargs["pk"]])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blogs/blog_delete.html"
    success_url = reverse_lazy("blogs:blog_list")