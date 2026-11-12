
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
