from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST
from datetime import date
from pathlib import Path
import json
import os
import tempfile
import threading
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.decorators.http import require_http_methods
from .api_views import _read_dealers

def get_cars(request):
    from django.http import JsonResponse

    cars = [
        {
            "id": 1,
            "name": "Toyota",
            "models": [
                {"id": 1, "name": "Camry"},
                {"id": 2, "name": "Corolla"},
                {"id": 3, "name": "RAV4"}
            ]
        },
        {
            "id": 2,
            "name": "Honda",
            "models": [
                {"id": 4, "name": "Civic"},
                {"id": 5, "name": "Accord"},
                {"id": 6, "name": "CR-V"}
            ]
        },
        {
            "id": 3,
            "name": "Ford",
            "models": [
                {"id": 7, "name": "Mustang"},
                {"id": 8, "name": "Explorer"},
                {"id": 9, "name": "Focus"}
            ]
        }
    ]

    return JsonResponse(cars, safe=False)

def analyze_review(request):
    from django.http import JsonResponse

    review = request.GET.get("text", "")

    positive_words = ["fantastic", "excellent", "great", "good", "amazing"]
    negative_words = ["bad", "poor", "terrible", "awful", "worst"]

    text = review.lower()

    if any(word in text for word in positive_words):
        sentiment = "positive"
    elif any(word in text for word in negative_words):
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return JsonResponse({
        "review": review,
        "sentiment": sentiment
    })


@require_http_methods(["GET", "POST"])
def user_login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", ""),
            password=request.POST.get("password", ""),
        )
        if user is not None and user.is_active:
            login(request, user)
            return redirect("home")
        return render(request, "login.html", {"error": "Invalid username or password."}, status=401)
    return render(request, "login.html")

@require_POST
def user_logout_page(request):
    logout(request)
    return redirect("home")



_review_write_lock = threading.Lock()


@require_http_methods(["GET", "POST"])
@login_required(login_url="/user-login/")
def post_dealer_review(request, dealer_id):
    dealer = next((d for d in (_read_dealers() or []) if d.get("id") == dealer_id), None)
    if dealer is None:
        raise Http404("Dealer not found")

    if request.method == "GET":
        return render(request, "post_review.html", {"dealer": dealer})

    name = request.POST.get("name", "").strip()
    review_text = request.POST.get("review", "").strip()
    purchase = request.POST.get("purchase", "").strip()
    make = request.POST.get("car_make", "").strip()
    model = request.POST.get("car_model", "").strip()
    year = request.POST.get("car_year", "").strip()
    error = None
    if not name or len(name) > 120 or not review_text or len(review_text) > 2000:
        error = "Please enter a name and review (maximum 2000 characters)."
    elif len(make) > 80 or len(model) > 80:
        error = "Car make and model must be 80 characters or fewer."
    elif purchase:
        try:
            date.fromisoformat(purchase)
        except ValueError:
            error = "Please enter a valid purchase date."
    if year:
        try:
            if not 1900 <= int(year) <= 2100:
                error = "Please enter a valid car year."
        except ValueError:
            error = "Please enter a valid car year."
    if error:
        return render(request, "post_review.html", {
            "dealer": dealer, "error": error, "form": request.POST
        }, status=400)

    positive = ("fantastic", "excellent", "great", "good", "amazing", "friendly", "helpful")
    negative = ("bad", "poor", "terrible", "awful", "worst")
    lower = review_text.casefold()
    sentiment = "positive" if any(word in lower for word in positive) else (
        "negative" if any(word in lower for word in negative) else "neutral"
    )
    path = Path(__file__).resolve().parent / "dealer_reviews.json"
    with _review_write_lock:
        try:
            reviews = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
            if not isinstance(reviews, list):
                raise ValueError("Invalid review storage")
            reviews.append({
                "id": max((int(r.get("id", 0)) for r in reviews if isinstance(r, dict)), default=0) + 1,
                "dealership": dealer_id,
                "name": name,
                "review": review_text,
                "purchase": purchase,
                "purchase_date": purchase,
                "car_make": make,
                "car_model": model,
                "car_year": int(year) if year else None,
                "sentiment": sentiment,
            })
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
                tmp_path = Path(tmp.name)
                json.dump(reviews, tmp, indent=2, ensure_ascii=False)
            os.replace(tmp_path, path)
        except (OSError, ValueError, TypeError):
            return render(request, "post_review.html", {
                "dealer": dealer, "error": "Unable to save your review. Please try again.",
                "form": request.POST,
            }, status=500)
    return redirect("dealer_details_page", dealer_id=dealer_id)


@require_http_methods(["GET"])
def get_course_cars(request):
    """Course-compatible endpoint returning the complete CarModels list."""
    from django.http import JsonResponse

    car_models = [
        {"CarMake": "Toyota", "CarModel": "Camry"},
        {"CarMake": "Toyota", "CarModel": "Corolla"},
        {"CarMake": "Toyota", "CarModel": "RAV4"},
        {"CarMake": "Honda", "CarModel": "Civic"},
        {"CarMake": "Honda", "CarModel": "Accord"},
        {"CarMake": "Honda", "CarModel": "CR-V"},
        {"CarMake": "Ford", "CarModel": "Mustang"},
        {"CarMake": "Ford", "CarModel": "Explorer"},
        {"CarMake": "Ford", "CarModel": "Focus"},
    ]
    return JsonResponse({"CarModels": car_models})


@require_http_methods(["GET"])
def analyze_review_path(request, review_text):
    """Sentiment analysis for the course-required /analyze/<review> URL."""
    from django.http import JsonResponse

    positive_words = ("fantastic", "excellent", "great", "good", "amazing")
    negative_words = ("bad", "poor", "terrible", "awful", "worst")
    normalized = review_text.casefold()
    sentiment = ("positive" if any(word in normalized for word in positive_words)
                 else "negative" if any(word in normalized for word in negative_words)
                 else "neutral")
    return JsonResponse({"review": review_text, "sentiment": sentiment})
