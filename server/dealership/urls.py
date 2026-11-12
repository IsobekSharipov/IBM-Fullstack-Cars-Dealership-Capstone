from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

def home(request):
    return HttpResponse("<h1>Cars Dealership</h1><p>Django server is running.</p>")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
]
