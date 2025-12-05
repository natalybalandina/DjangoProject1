from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (HomeView, ProductDetailView, ContactsView, ProductCreateView, ProductUpdateView, ProductDeleteView, CategoryView, ProductPublishView)
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path("product_info/<int:pk>/", ProductDetailView.as_view(), name="product_info"),
    path("add_product/", ProductCreateView.as_view(), name="add_product"),
    path('edit-product/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('delete-product/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category_view'),
    path('unpublish-product/<int:pk>/', views.UnpublishProductView.as_view(), name='unpublish_product'),
    path('toggle-publish/<int:pk>/', views.TogglePublishProductView.as_view(), name='toggle_publish'),
    path('unpublish-product/<int:pk>/confirm/', views.UnpublishProductConfirmView.as_view(), name='unpublish_product_confirm'),
]