from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (HomeView, ProductDetailView, ContactsView, ProductCreateView, ProductUpdateView, ProductDeleteView, CategoryView)


app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path("product_info/<int:pk>/", ProductDetailView.as_view(), name="product_info"),
    path("add_product/", ProductCreateView.as_view(), name="add_product"),
    path('edit-product/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('delete-product/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category_view'),
]