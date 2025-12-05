from django.forms import ModelForm
from django import forms

from blogs.models import BlogPost


class BlogPostForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content", "preview_image", "publication_sign"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите заголовок поста",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите содержание поста",
                }
            ),
            "preview_image": forms.FileInput(attrs={"class": "form-control-file"}),
            "publication_sign": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }