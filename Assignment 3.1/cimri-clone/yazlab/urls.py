"""yazlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from laptop.views import laptop_list, laptop_info, SearchResultsView, my_filter
from django_filters.views import FilterView
from laptop.filters import LaptopFilter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', laptop_list),
    path('laptop/<pk>/', laptop_info),
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path("laptop_list/", FilterView.as_view(filterset_class=LaptopFilter,
    template_name='laptop_list.html'), name='my_filter'),
]
