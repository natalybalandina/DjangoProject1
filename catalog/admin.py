from django.contrib import admin
from django.core.cache import cache
from django.urls import reverse
from django.urls import path
from django.utils.html import format_html
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from catalog.models import Category, Product, Contact
from .forms import ProductForm


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ("id", "name", "price", "category", "is_published")
    list_filter = ("category", "is_published")
    search_fields = ("name", "description")
    change_list_template = 'admin/catalog/product/change_list.html'  # Добавляем кастомный шаблон

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'clear-cache/',
                self.admin_site.admin_view(self.clear_cache),
                name='product_clear_cache'
            ),
        ]
        return custom_urls + urls

    def clear_cache(self, request):
        cache.clear()
        self.message_user(request, "Кеш успешно очищен")
        return redirect("admin:catalog_product_changelist")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['clear_cache_url'] = reverse('admin:product_clear_cache')
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name", "description")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone")
    search_fields = ("name", "phone", "email")