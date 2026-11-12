
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

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

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
