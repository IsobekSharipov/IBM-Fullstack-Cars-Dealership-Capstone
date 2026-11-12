from django.contrib import admin
from django.shortcuts import render
from .api_views import _read_dealers
from django.urls import path
from .api_views import (login_user, logout_user, get_dealer_reviews,
                        get_all_dealers, get_dealer_by_id, get_dealers_by_state)


def home(request):
    dealers = _read_dealers() or []
    state = request.GET.get("state", "").strip()
    if state:
        dealers = [d for d in dealers if d.get("state", "").casefold() == state.casefold() or d.get("st", "").casefold() == state.casefold()]
    return render(request, "home.html", {"dealers": dealers, "selected_state": state})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("login", login_user, name="login_user"),
    path("logout", logout_user, name="logout_user"),
    path("get_reviews/<int:dealer_id>", get_dealer_reviews, name="get_dealer_reviews"),
    path("get_dealers", get_all_dealers, name="get_all_dealers"),
    path("get_dealers/<int:dealer_id>", get_dealer_by_id, name="get_dealer_by_id"),
    path("get_dealers/state/<str:state>", get_dealers_by_state, name="get_dealers_by_state"),
]

from .views import get_cars

urlpatterns += [
    path("get_cars", get_cars, name="get_cars"),
]

from .views import analyze_review

urlpatterns += [
    path("analyze_review", analyze_review, name="analyze_review"),
]

from .views import user_login_page, user_logout_page

urlpatterns += [
    path("user-login/", user_login_page, name="user_login_page"),
    path("user-logout/", user_logout_page, name="user_logout_page"),
]
