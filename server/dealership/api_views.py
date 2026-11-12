import json
from pathlib import Path

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST


def _read_credentials(request):
    try:
        payload = json.loads(request.body)
        if not isinstance(payload, dict):
            raise ValueError("Expected JSON object")
        return payload
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        return None


@csrf_exempt
@require_POST
def login_user(request):
    """JSON login endpoint for the course's cURL API exercise."""
    data = _read_credentials(request)
    if data is None:
        return JsonResponse({"message": "Invalid JSON payload"}, status=400)
    username = data.get("username")
    password = data.get("password")
    if not isinstance(username, str) or not isinstance(password, str):
        return JsonResponse({"message": "Username and password are required"}, status=400)
    user = authenticate(request, username=username, password=password)
    if user is None or not user.is_active:
        return JsonResponse({"message": "Invalid username or password"}, status=401)
    login(request, user)
    return JsonResponse({"message": "Login successful", "username": user.get_username()})


@csrf_exempt
@require_POST
def logout_user(request):
    """JSON logout endpoint for the course's cURL API exercise."""
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Not logged in"}, status=401)
    logout(request)
    return JsonResponse({"message": "Logout successful"})


@require_GET
def get_dealer_reviews(request, dealer_id):
    """Return stored reviews for a dealer, as JSON."""
    reviews_path = Path(__file__).resolve().parent / "dealer_reviews.json"
    if not reviews_path.exists():
        return JsonResponse([], safe=False)
    try:
        with reviews_path.open(encoding="utf-8") as source:
            reviews = json.load(source)
    except (OSError, json.JSONDecodeError):
        return JsonResponse({"message": "Review data unavailable"}, status=500)
    if not isinstance(reviews, list):
        return JsonResponse({"message": "Invalid review data"}, status=500)
    filtered = [review for review in reviews if isinstance(review, dict) and str(review.get("dealership")) == str(dealer_id)]
    return JsonResponse(filtered, safe=False)
