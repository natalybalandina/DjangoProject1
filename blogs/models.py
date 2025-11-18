from django.db import models


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок поста",
        help_text="Введите заголовок поста",
    )
    content = models.TextField(
        verbose_name="Содержание поста", help_text="Введите содержание поста"
    )
    preview_image = models.ImageField(
        upload_to="blog_posts/preview_images", verbose_name="Превью изображение поста"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    publication_sign = models.BooleanField(
        default=False, verbose_name="Публикация поста", help_text="Опубликовать пост?"
    )
    count_views = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество просмотров",
        help_text="Укажите количество просмотров поста",
        editable=False
    )

    class Meta:
        verbose_name = "Блог пост"
        verbose_name_plural = "Блог посты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
