import os
import googleapiclient.discovery
import random
api_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
search_engine = os.environ.get("GOOGLE_SEARCH_ENGINE")

service = googleapiclient.discovery.build(
        "customsearch", "v1", developerKey=api_key)


def image_search(query):
    response = service.cse().list(
                q=query,
                cx=search_engine,
                lr="lang_ja",
                start=1
            ).execute()

    items = response["items"]
    pagemaps = [item["pagemap"] for item in items]
    cse_images = [pagemap["cse_image"] for pagemap in pagemaps]
    return [c["src"]
            for cse_image in cse_images
            for c in cse_image
            if c["src"].startswith("https")]


def only_https(url_list):
    return [url for url in url_list if url.startswith("https")]


def one(query):
    url_list = image_search(query)
    return random.choice(only_https(url_list))
