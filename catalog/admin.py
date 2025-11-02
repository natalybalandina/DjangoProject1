from django.contrib import admin
from catalog.models import Category, Product, Contact


def format_datetime(value):
    if value is not None:
        return value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return ""


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "formatted_created_at", "formatted_updated_at", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")

    def formatted_created_at(self, obj):
        return format_datetime(obj.created_at)

    def formatted_updated_at(self, obj):
        return format_datetime(obj.updated_at)

    formatted_created_at.short_description = 'Created At'
    formatted_updated_at.short_description = 'Updated At'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name", "description")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone")
    search_fields = ("name", "phone", "email")
