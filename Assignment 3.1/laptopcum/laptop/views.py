from django.shortcuts import render

from laptop.models import Laptop



def laptop_list(request):
    laptops = Laptop.objects.all()
    context = {
        "laptops": laptops
    }
    return render(request, "main.html", context)

def laptop_info(request, pk):
    laptop = Laptop.objects.get(id=pk)
    context = {
        "laptop": laptop
    }
    return render(request, "laptop.html", context)
