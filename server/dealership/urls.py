from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from .api_views import login_user, logout_user, get_dealer_reviews


def home(request):
    return HttpResponse("<h1>Cars Dealership</h1><p>Django server is running.</p>")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("login", login_user, name="login_user"),
    path("logout", logout_user, name="logout_user"),
    path("get_reviews/<int:dealer_id>", get_dealer_reviews, name="get_dealer_reviews"),
]
