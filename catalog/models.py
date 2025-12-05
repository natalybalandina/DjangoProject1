from django.db import models
from django import forms
from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название категории",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

PUBLISH_STATUS = [
    ('draft', 'Черновик'),
    ('published', 'Опубликовано'),
    ('archived', 'В архиве'),
]

class Product(models.Model):
    status = models.CharField(
        max_length=20,
        choices=PUBLISH_STATUS,
        default='draft',
        verbose_name="Статус публикации"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Владелец продукта",
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название продукта",
        help_text="Введите название продукта",
    )
    description = models.TextField(
        verbose_name="Описание продукта",
        help_text="Введите описание продукта",
        blank=True,
        null=True,
    )
    publication_status = models.CharField(
        max_length=20,
        choices=PUBLISH_STATUS,
        default='draft',
        verbose_name="Статус публикации"
    )
    image = models.ImageField(
        upload_to="catalog/photo",
        blank=True,
        null=True,
        help_text="Загрузите изображение продукта",
        verbose_name="Изображение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        null=True,
        blank=True,
        related_name="products",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Активен ли товар в каталоге"
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Публиковать товар в каталоге"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
            ("can_change_product_status", "Can change product status"),
            ('can_delete_product', 'Can delete product'),
        ]


class ContactInfo(models.Model):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"Contact Info - {self.address}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name
