from django.utils.decorators import method_decorator
from django.views import View
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from blogs.models import BlogPost
from catalog.models import Product, Contact, Category
from catalog.forms import ProductForm
from catalog.services import get_products_by_category


class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products_list'
    paginate_by = 6

    def get_queryset(self):
        cache_key = f"product_list_queryset:page_{self.request.GET.get('page', 1)}:search_{self.request.GET.get('q', '')}"
        search_query = self.request.GET.get('q', '')

        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = Product.objects.filter(publication_status='published')

            if search_query:
                queryset = queryset.filter(
                    Q(name__icontains=search_query) |
                    Q(description__icontains=search_query) |
                    Q(category__name__icontains=search_query)
                )

            queryset = queryset.order_by('id')
            cache.set(cache_key, queryset, 300)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.all()
        context['can_delete_product'] = 'catalog.can_delete_product'
        context['latest_blogs'] = BlogPost.objects.filter(
            publication_sign=True
        ).order_by('-created_at')[:3]
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_info.html'
    context_object_name = 'product'

    @method_decorator(cache_page(60 * 15))  # Кеширование на 15 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.all()
        context['latest_products'] = Product.objects.all().order_by("-created_at")[:5]
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        telephone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо {name} за отзыв! Ваше сообщение получено")

class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:home')
    success_message = "Продукт успешно добавлен!"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        new_category_name = form.cleaned_data.get('new_category_name', '').strip()
        category = form.cleaned_data.get('category')

        if category:
            return super().form_valid(form)
        elif new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            product = form.save(commit=False)
            product.category = category
            product.save()
            self.success_message = f"Создана новая категория '{category.name}' и продукт добавлен!"
            return redirect(self.success_url)
        else:
            form.add_error(None, "Выберите существующую категорию или укажите новую")
            return self.form_invalid(form)

class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/edit_product.html'
    success_url = reverse_lazy('catalog:home')
    success_message = "Продукт успешно обновлен!"

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return user == product.owner or user.has_perm('catalog.can_change_product_status')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        # Разрешаем удаление:
        # - владельцу продукта
        # - пользователям с правом can_delete_product
        # - staff пользователям
        if not (product.owner == request.user or
                request.user.has_perm('catalog.can_delete_product') or
                request.user.is_staff):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/delete_product.html'
    success_url = reverse_lazy('catalog:home')

    # Пример проверки в представлении
    def edit_product(request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not (request.user == product.owner or request.user.is_staff):
            raise PermissionDenied
        # остальной код представления

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().post(request, *args, **kwargs)

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return user == product.owner or user.has_perm('catalog.delete_product')


class ProductPublishView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_change_product_status'
    model = Product
    fields = ['publication_status']
    template_name = 'catalog/unpublish_product.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Статус продукта изменен на {self.object.get_publication_status_display()}")
        return response

class CategoryView(ListView):
    model = Product
    template_name = 'category.html'
    paginate_by = 6
    context_object_name = 'products'

    # def get_queryset(self):
    #     category_id = self.kwargs.get('category_id')
    #     self.category = Category.objects.get(id=category_id)
    #     return Product.objects.filter(category=self.category).order_by('id')
    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Category.DoesNotExist:
            return render(request, 'catalog/catalog/category_not_found.html', {'category_id': kwargs['category_id']})


class UnpublishProductView(PermissionRequiredMixin, TemplateView):
    permission_required = 'catalog.can_unpublish_product'
    template_name = 'catalog/unpublish_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        if not product.is_published:
            messages.error(self.request, "Этот товар уже не опубликован")
            raise PermissionDenied
        context['product'] = product
        return context


class UnpublishProductConfirmView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not product.is_published:
            messages.error(request, "Этот товар уже не опубликован")
            return redirect('catalog:product_info', pk=product.pk)

        product.is_published = False
        product.save()
        messages.success(request, f"Товар '{product.name}' успешно снят с публикации")
        return redirect('catalog:product_info', pk=product.pk)


class TogglePublishProductView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'
    template_name = 'catalog/unpublish_product.html'

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, self.template_name, {'product': product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = not product.is_published
        product.save()
        action = "снят с публикации" if not product.is_published else "опубликован"
        messages.success(request, f"Товар '{product.name}' {action}")
        return redirect('catalog:product_info', pk=product.pk)