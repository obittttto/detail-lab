from django.shortcuts import render
from .models import Service

def home(request):
    services = Service.objects.filter(is_active=True)

    context = {
        "services": services,
    }

    return render(request, "home.html", context)


# Create your views here.
