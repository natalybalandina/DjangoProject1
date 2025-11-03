from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from catalog.forms import ProductForm
from catalog.models import Product, Contact, Category
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied


def home(request):
    search_query = request.GET.get('q', '')
    if search_query:
        products_list = Product.objects.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)  # Добавляем поиск по категории
        )
    else:
        products_list = Product.objects.all()

    categories = Category.objects.all()  # Получаем все категории

    context = {
        'products_list': products_list,
        'search_query': search_query,
        'categories': categories,  # Передаём категории в контекст
    }
    print(f"Query: {search_query}")
    print(f"Products: {products_list}")
    return render(request, 'home.html', context)


def product_info(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "product_info.html", context)


def contacts(request):
    contacts_data = Contact.objects.all()
    latest_products = Product.objects.all().order_by("-created_at")[:5]

    if request.method == 'POST':
        name = request.POST.get('name')
        telephone = request.POST.get('phone')
        message = request.POST.get('message')

        return HttpResponse(f"Спасибо {name} за отзыв! Ваше сообщение получено")

    return render(
        request,
        "contacts.html",
        {"contacts": contacts_data, "latest_products": latest_products},
    )


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_category_name = form.cleaned_data.get('new_category_name', '').strip()
            category = form.cleaned_data.get('category')

            # Если выбрана существующая категория
            if category:
                product = form.save()
                messages.success(request, "Продукт успешно добавлен!")
                return redirect('catalog:home')

            # Если указана новая категория
            elif new_category_name:
                category, created = Category.objects.get_or_create(name=new_category_name)
                product = form.save(commit=False)
                product.category = category
                product.save()
                messages.success(request, f"Создана новая категория '{category.name}' и продукт добавлен!")
                return redirect('catalog:home')

            # Если ни одна категория не указана
            else:
                messages.error(request, "Выберите существующую категорию или укажите новую")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме")
    else:
        form = ProductForm()

    # Проверка генерации ID
    print("\nПроверка ID полей:")
    for field_name, field in form.fields.items():
        print(f"{field_name}: {field.widget.attrs.get('id', 'auto')}")

    return render(request, "add_product.html", {'form': form})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})

@require_POST
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Дополнительная проверка прав (если нужно)
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        product.delete()
        return redirect('catalog:home')

    return render(request, 'delete_product.html', {'product': product})


def category_view(request, category_id):
    """Отображает список товаров по категории"""
    try:
        category = Category.objects.get(id=category_id)
        product_list = Product.objects.filter(category=category).order_by('id')

        # Пагинация
        paginator = Paginator(product_list, 6)  # 6 продуктов на странице
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

        context = {
            'category': category,
            'products': products,
        }
        return render(request, 'category.html', context)
    except Category.DoesNotExist:
        return render(request, 'category_not_found.html', {'category_id': category_id})
