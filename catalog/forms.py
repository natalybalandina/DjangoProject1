from django import forms
from .models import Product
from django.core.exceptions import ValidationError

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    new_category_name = forms.CharField(
        required=False,
        label="Новая категория",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_new_category_name'
        })
    )

    is_active = forms.BooleanField(
        label="Активный товар",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image', 'is_active']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_category'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_name',
                'placeholder': 'Введите название продукта'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'id_description',
                'rows': 3,
                'placeholder': 'Введите описание продукта'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'id_price',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'id_image'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            elif field_name != 'image':
                field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        for word in FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(f'Название содержит запрещенное слово: {word}')
        return self.cleaned_data['name']

    def clean_description(self):
        description = self.cleaned_data['description'].lower()
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError(f'Описание содержит запрещенное слово: {word}')
        return self.cleaned_data['description']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер файла не должен превышать 5MB')

            valid_extensions = ['.jpg', '.jpeg', '.png']
            extension = image.name.split('.')[-1].lower()
            if f'.{extension}' not in valid_extensions:
                raise ValidationError('Поддерживаются только файлы JPEG и PNG')
        return image
