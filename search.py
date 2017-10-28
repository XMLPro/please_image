import os
import googleapiclient.discovery
import random
import requests
api_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
search_engine = os.environ.get("GOOGLE_SEARCH_ENGINE")

base_dir = os.path.dirname(os.path.abspath(__file__))

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
    pagemaps = [item.get("pagemap") for item in items]
    cse_images = [pagemap.get("cse_image") for pagemap in pagemaps if pagemap]
    return [c["src"]
            for cse_image in cse_images
            if cse_image
            for c in cse_image]


def only_https(url_list):
    return [url for url in url_list if url.startswith("https")]


def one(query):
    url_list = image_search(query)
    return random.choice(only_https(url_list))


# get root like this: request.url_root
def one_include_http(query, root):
    url = random.choice(image_search(query))
    if url.startswith("https"):
        return url
    image = requests.get(url)
    save_name = "static/image/TMP_IMAGE." + url.split(".")[-1]
    save_path = base_dir + "/" + save_name
    if image.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(image.content)
    return root + save_name
