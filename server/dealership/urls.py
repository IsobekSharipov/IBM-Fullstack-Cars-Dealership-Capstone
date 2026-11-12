from django.contrib import admin
from django.shortcuts import render
from .api_views import _read_dealers
from django.urls import path
from .api_views import (
    login_user, logout_user, get_dealer_reviews,
    get_all_dealers, get_dealer_by_id, get_dealers_by_state,
)
from .views import get_cars, get_course_cars
from .views import analyze_review, analyze_review_path
from .views import user_login_page, user_logout_page
from django.http import Http404
from .views import post_dealer_review


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
    path("djangoapp/login", login_user, name="djangoapp_login"),
    path("logout", logout_user, name="logout_user"),
    path("djangoapp/logout", logout_user, name="djangoapp_logout"),
    path("get_reviews/<int:dealer_id>", get_dealer_reviews, name="get_dealer_reviews"),
    path("fetchReviews/dealer/<int:dealer_id>", get_dealer_reviews, name="fetch_dealer_reviews"),
    path("get_dealers", get_all_dealers, name="get_all_dealers"),
    path("fetchDealers", get_all_dealers, name="fetch_dealers"),
    path("get_dealers/<int:dealer_id>", get_dealer_by_id, name="get_dealer_by_id"),
    path("get_dealers/state/<str:state>", get_dealers_by_state, name="get_dealers_by_state"),
]


urlpatterns += [
    path("get_cars", get_cars, name="get_cars"),
    path("djangoapp/get_cars", get_course_cars, name="djangoapp_get_cars"),
]


urlpatterns += [
    path("analyze_review", analyze_review, name="analyze_review"),
    path("analyze/<path:review_text>", analyze_review_path, name="analyze_review_path"),
]


urlpatterns += [
    path("user-login/", user_login_page, name="user_login_page"),
    path("user-logout/", user_logout_page, name="user_logout_page"),
]


def dealer_details_page(request, dealer_id):
    dealer = next((d for d in (_read_dealers() or []) if d.get("id") == dealer_id), None)
    if dealer is None:
        raise Http404("Dealer not found")
    from pathlib import Path
    import json
    reviews_file = Path(__file__).resolve().parent / "dealer_reviews.json"
    reviews = []
    if reviews_file.exists():
        try:
            data = json.loads(reviews_file.read_text(encoding="utf-8"))
            if isinstance(data, list):
                reviews = [item for item in data if isinstance(item, dict) and str(item.get("dealership")) == str(dealer_id)]
        except (OSError, ValueError):
            pass
    return render(request, "dealer_details.html", {"dealer": dealer, "reviews": reviews})

urlpatterns += [
    path("dealers/<int:dealer_id>/", dealer_details_page, name="dealer_details_page"),
]


urlpatterns += [
    path("dealers/<int:dealer_id>/review/", post_dealer_review, name="post_dealer_review"),
]
