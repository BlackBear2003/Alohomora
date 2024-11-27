import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter
import urllib.parse


router = APIRouter()

pp_url = "http://81.68.212.127:5010"


def get_proxy():
    return requests.get(pp_url + "/get/").json()


def rm_proxy(proxy):
    requests.get(pp_url + "/delete/?proxy={}".format(proxy))


@router.get("/api/crawl/note")
async def crawl_note(url: str):
    decoded_url = urllib.parse.unquote(url)
    # 启动爬虫抓取指定 URL 的数据
    result = crawl_note_img(decoded_url)
    return {"status": "success", "data": result}


def crawl_note_img(url: str):
    html = get_html(url)
    if not html:
        return []
    soup = BeautifulSoup(html.text, 'html.parser')
    print(soup)

    # 查找所有带有 data-xhs-img 属性的 img 标签
    images = soup.find_all('meta', {'name': 'og:image'})
    print(images)

    # 提取图片 URL
    image_urls = [img['content'] for img in images if 'content' in img.attrs]
    print(image_urls)

    return image_urls


def get_html(url: str):
    retry = 5
    proxy = get_proxy().get("proxy")
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}

    while retry > 0:
        try:
            response = requests.get(url, proxies={"http": "http://{}".format(proxy)}, headers=headers)
            return response
        except Exception:
            retry -= 1
    rm_proxy(proxy)
    return None
