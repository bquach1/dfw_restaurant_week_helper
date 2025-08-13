import os
from dotenv import load_dotenv
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET

# Load .env file from project root (adjust path if needed)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")


@require_GET
def get_restaurant_info(request):
    name = request.GET.get("name")
    if not name:
        return JsonResponse({"error": "Missing restaurant name"}, status=400)

    print(GOOGLE_PLACES_API_KEY)

    # Step 1: Find place_id
    find_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    find_params = {
        "input": name,
        "inputtype": "textquery",
        "fields": "place_id",
        "key": GOOGLE_PLACES_API_KEY,
    }
    find_resp = requests.get(find_url, params=find_params)
    find_data = find_resp.json()
    candidates = find_data.get("candidates", [])
    if not candidates:
        return JsonResponse({"error": "No place found"}, status=404)
    place_id = candidates[0]["place_id"]

    # Step 2: Get place details
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    details_params = {
        "place_id": place_id,
        "fields": "name,formatted_address,geometry,types,website,international_phone_number,rating,review,user_ratings_total",
        "key": GOOGLE_PLACES_API_KEY,
    }
    details_resp = requests.get(details_url, params=details_params)
    details_data = details_resp.json()

    return JsonResponse(details_data)
