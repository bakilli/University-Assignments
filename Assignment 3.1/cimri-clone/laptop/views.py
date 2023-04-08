from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q, Count
from .filters import LaptopFilter
import django_filters
from .filters import LaptopFilter

from laptop.models import Laptop


def laptop_list(request):
    laptops = Laptop.objects.all()
    context = {
        "laptops": laptops
    }
    return render(request, "main.html", context)


def laptop_info(request, pk):
    laptop = Laptop.objects.get(id=pk)
    linkler = Laptop.objects.filter(model=laptop.model).order_by('price')[:3]
    context = {
        "laptop": laptop,
        "linkler": linkler
    }
    return render(request, "laptop.html", context)


class SearchResultsView(ListView):
    model = Laptop
    template_name = "search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Laptop.objects.filter(
            Q(name__icontains=query))
        return object_list


def my_filter(request):
    laptop_list = Laptop.objects.all()
    laptop_filter = LaptopFilter(request.GET, queryset=laptop_list)
    return render(request, 'laptop_list.html', {'filter': laptop_filter})




# def testing(request):
#     # laptops = Laptop.objects.raw('SELECT *'
#     #                              'FROM laptop_laptop'
#     #                              ''
#     #                              'GROUP BY model')
#     # laptops = Laptop.objects.all().group_by('model')
#     # laptops = Laptop.objects.all().annotate(dcount=Count('model')).order_by('-dcount')
#     laptops = Laptop.objects.raw('''select id, name, brand, model, operating_system, cpu, gpu, ram, disc, 
#                                            disc_type, screen_size, rating, price, site, site_link
#                                     from (
#                                     SELECT row_number() over(partition by model) row_id, *
#                                     FROM laptop_laptop  ) x
#                                     where x.row_id = 1''')
#     context = {
#         "laptops": laptops
#     }
#     return render(request, "main.html", context)
