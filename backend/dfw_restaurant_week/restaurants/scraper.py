import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Load .env from parent directory (adjust path as needed)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))


def scrape_and_store():
    url = "https://www.dfwrestaurantweek.com/reservations"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    mongodb_password = os.environ.get("MONGODB_PASSWORD")
    client = MongoClient(
        f"mongodb+srv://quachbruce:{mongodb_password}@cluster0.qatixef.mongodb.net/"
    )
    db = client["dfw_restaurant_week"]
    collection = db["restaurants"]

    # Find all restaurant names
    restaurants = soup.find_all(
        "h3", class_="mb-1 restaurant-filter_dining_card_headline__k0Wkm"
    )
    for r in restaurants:
        name = r.get_text(strip=True)
        collection.update_one({"name": name}, {"$set": {"name": name}}, upsert=True)

    print(f"Stored {len(restaurants)} restaurants in MongoDB.")


if __name__ == "__main__":
    scrape_and_store()
