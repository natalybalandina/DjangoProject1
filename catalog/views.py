from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect, render, HttpResponse
from django.core.exceptions import PermissionDenied

from catalog.models import Product, Contact, Category
from catalog.forms import ProductForm

class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products_list'
    paginate_by = 6

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        queryset = Product.objects.all()  # Получаем все продукты

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )

        return queryset.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_info.html'
    context_object_name = 'product'

class ContactsView(TemplateView):
    template_name = 'contacts.html'

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

class ProductCreateView(SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('catalog:home')
    success_message = "Продукт успешно добавлен!"

    def form_valid(self, form):
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

class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'edit_product.html'
    success_url = reverse_lazy('catalog:home')
    success_message = "Продукт успешно обновлен!"

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('catalog:home')

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().post(request, *args, **kwargs)

class CategoryView(ListView):
    model = Product
    template_name = 'category.html'
    paginate_by = 6
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        self.category = Category.objects.get(id=category_id)
        return Product.objects.filter(category=self.category).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Category.DoesNotExist:
            return render(request, 'categories_not_database.html', {'category_id': kwargs['category_id']})