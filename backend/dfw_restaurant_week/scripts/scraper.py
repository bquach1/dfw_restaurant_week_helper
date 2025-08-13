import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import io
from PyPDF2 import PdfReader

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))


def extract_pdf_text(pdf_data):
    pdf_stream = io.BytesIO(pdf_data)
    reader = PdfReader(pdf_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def scrape_and_store():
    base_url = "https://www.dfwrestaurantweek.com"
    url = f"{base_url}/reservations"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    mongodb_password = os.environ.get("MONGODB_PASSWORD")
    client = MongoClient(
        f"mongodb+srv://quachbruce:{mongodb_password}@cluster0.qatixef.mongodb.net/"
    )
    db = client["dfw_restaurant_week"]
    collection = db["restaurants"]

    # Find all restaurant <a> tags with href starting with /restaurant/
    restaurant_links = soup.select('a[href^="/restaurant/"]')

    for index, link in enumerate(restaurant_links):
        name_tag = link.find("h3")
        if not name_tag:
            continue
        name = name_tag.get_text(strip=True) if name_tag else None

        # Get menu page URL from href
        menu_url = base_url + link["href"]

        pdf_data = None
        pdf_url = None
        # If menu_url exists, fetch the menu page and get PDF
        if menu_url:
            menu_resp = requests.get(menu_url)
            menu_soup = BeautifulSoup(menu_resp.text, "html.parser")
            iframe = menu_soup.find("iframe", src=True, title="PDF Viewer")
            if iframe:
                pdf_url = iframe["src"]
                if pdf_url.lower().endswith(".pdf"):
                    pdf_resp = requests.get(pdf_url)
                    if (
                        pdf_resp.status_code == 200
                        and "application/pdf"
                        in pdf_resp.headers.get("Content-Type", "")
                    ):
                        pdf_data = extract_pdf_text(pdf_resp.content)
                else:
                    print(f"Skipped non-PDF iframe src: {pdf_url}")

        # Upload to MongoDB
        collection.update_one(
            {"name": name},
            {
                "$set": {
                    "name": name,
                    "menu_url": menu_url,
                    "pdf_url": pdf_url,
                    "pdf_data": pdf_data,
                }
            },
            upsert=True,
        )

        print(f"Processed {index + 1}/{len(restaurant_links)}: {name}")

    print(f"Scraped and stored {len(restaurant_links)} restaurants with menu info.")


if __name__ == "__main__":
    scrape_and_store()
