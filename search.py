import os
import googleapiclient.discovery
import random
import requests
import itertools
api_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
search_engine = os.environ.get("GOOGLE_SEARCH_ENGINE")

base_dir = os.path.dirname(os.path.abspath(__file__))

service = googleapiclient.discovery.build(
        "customsearch", "v1", developerKey=api_key)

name_parts = list(itertools.chain(
        range(ord("a"), ord("z") + 1),
        range(ord("A"), ord("Z") + 1),
        range(ord("0"), ord("9") + 1),
        ))

def image_search(query):
    return ["http://www.teu.ac.jp/infomation/2014/images/2014CS_gakubucho.jpg"]
    # response = service.cse().list(
    #             q=query,
    #             cx=search_engine,
    #             lr="lang_ja",
    #             num=10,
    #             start=1,
    #             searchType="image"
    #         ).execute()
    # items = response["items"]
    # return [item.get("link") for item in items]


def only_https(url_list):
    return [url for url in url_list if url.startswith("https")]


def one(query):
    url_list = image_search(query)
    return random.choice(only_https(url_list))


def random_name(length):
    return "".join(chr(random.choice(name_parts)) for x in range(length))


def delete_files(dir_name):
    [os.remove(x) for x in os.listdir(base_dir+ "/static/image/line/") if not x.startswith(".")]
    for filename in os.listdir(dir_name):
        if not filename.startswith("."):
            os.remove(filename)


# get root like this: request.url_root
def one_include_http(query, root):
    url = random.choice(image_search(query))
    if url.startswith("https"):
        return url
    image = requests.get(url)
    save_dir = "static/image/line/"
    save_name = "{}{}.{}".format(save_dir, random_name(30), url.split(".")[-1])
    save_path = "{}/{}".format(base_dir, save_name)
    delete_files("{}/{}".format(base_dir, save_dir))
    if image.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(image.content)
    return root + save_name
