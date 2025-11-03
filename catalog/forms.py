from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    new_category_name = forms.CharField(
        required=False,
        label="Новая категория",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_new_category_name'
        })
    )

    class Meta:
        model = Product
        fields = ['category', 'new_category_name', 'name', 'description', 'price', 'image']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_category'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'id_description',
                'rows': 3
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'id_price',
                'step': '0.01'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'id_image'
            })
        }
