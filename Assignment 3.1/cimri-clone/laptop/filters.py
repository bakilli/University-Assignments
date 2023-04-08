import django_filters
from django import forms

from .models import Laptop


brand_choices = (
    ('Acer', 'Acer'),
    ('Apple', 'Apple'),
    ('Asus', 'Asus'),
    ('Casper', 'Casper'),
    ('Dell', 'Dell'),
    ('Fujitsu', 'Fujitsu'),
    ('HP', 'HP'),
    ('Huawei', 'Huawei'),
    ('Msi', 'Msi'),
    ('Monster', 'Monster'),
    ('Lenovo', 'Lenovo'),
    ('Toshiba', 'Toshiba'),
)

op_choices = (
    ('Windows 11', 'Windows 11'),
    ('Windows 10', 'Windows 10'),
    ('Windows', 'Windows'),
    ('MacOS', 'MacOS'),
    ('Linux', 'Linux'),
    ('Ubuntu', 'Ubuntu'),
    ('FreeDos', 'FreeDos'),
)

cpu_choices = (
    
    ('i3', 'Intel Core i3'),
    ('i5', 'Intel Core i5'),
    ('i7', 'Intel Core i7'),
    ('i9', 'Intel Core i9'),
    ('Celeron', 'Intel Celeron'),
    ('M1', 'M1'),
    ('M2', 'M2'),
    ('Amd Ryzen 3', 'Amd Ryzen 3'),
    ('Amd Ryzen 5', 'Amd Ryzen 5'),
    ('Amd Ryzen 7', 'Amd Ryzen 7'),
    ('Amd Ryzen 9', 'Amd Ryzen 9'),
    ('Xeon', 'Intel Xeon'),
    ('Pentium', 'Intel Pentium'),
)

gpu_choices = (
    ('Nvidia', 'Nvidia'),
    ('AMD', 'AMD'),
    ('Intel', 'Intel'),
)

site_choices = (
    ('amazon',       'Amazon'),
    ('n11',          'N11'),
    ('teknosa',      'Teknosa'),
    ('vatan',        'Vatan'),
    ('laptopcum',    'Laptopcum'),
    
)

class LaptopFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    model = django_filters.CharFilter(lookup_expr='icontains')
    ram = django_filters.RangeFilter()
    brand = django_filters.MultipleChoiceFilter(choices=brand_choices, widget = forms.CheckboxSelectMultiple(), lookup_expr='icontains')
    price = django_filters.RangeFilter()
    rating = django_filters.RangeFilter()
    disc = django_filters.RangeFilter()
    operating_system = django_filters.MultipleChoiceFilter(choices=op_choices, widget = forms.CheckboxSelectMultiple(), lookup_expr='icontains')
    screen_size = django_filters.RangeFilter()
    cpu = django_filters.MultipleChoiceFilter(choices=cpu_choices, widget = forms.CheckboxSelectMultiple(), lookup_expr='icontains')
    gpu = django_filters.MultipleChoiceFilter(choices=gpu_choices, widget = forms.CheckboxSelectMultiple(), lookup_expr='icontains')
    site = django_filters.MultipleChoiceFilter(choices=site_choices, widget = forms.CheckboxSelectMultiple(), lookup_expr='icontains')
    o = django_filters.OrderingFilter(fields=(
            ('price', 'price'),
            ('rating', 'rating'),
            ))
    class Meta:
        model = Laptop
        fields = ['operating_system']
