from requests.exceptions import RequestException
import json
import requests

def crawl_amazon_product_details(url: str) -> str:
    API_TOKEN = "<Crawlbase Normal requests token>"
    API_ENDPOINT = "https://api.crawlbase.com/"

    params = {
        "token": API_TOKEN,
        "url": url,
        "scraper": "amazon-product-details"
    }

    response = requests.get(API_ENDPOINT, params=params)
    response.raise_for_status()

    product_json = json.loads(response.text)

    data = {
        "url": product_json["body"]["canonicalUrl"],
        "price": product_json["body"]["rawPrice"],
        "currency": product_json["body"]["currency"],
        "name": product_json["body"]["name"]
    }

    required_fields = ["price", "name", "url", "currency"]
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        raise ValueError(f"Data extraction failed: Missing required fields: {', '.join(missing_fields)}")

    return data
