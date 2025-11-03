from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, product_info, add_product, edit_product, delete_product, category_view


app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path("product_info/<int:pk>/", product_info, name="product_info"),
    path("add_product/", add_product, name="add_product"),
    path('edit-product/<int:pk>/', edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', delete_product, name='delete_product'),
    path('category/<int:category_id>/', category_view, name='category_view'),
    path('products/add/', add_product, name='product_add'),  # Более RESTful URL
]
