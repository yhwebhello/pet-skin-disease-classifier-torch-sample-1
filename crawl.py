import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime
import time

def download_image(url, file_path):
    # URL이 상대 경로인 경우 절대 URL로 변환
    if not url.startswith("http"):
        url = urljoin("https://www.google.com/", url)

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def get_image_urls(search_query, num_images):
    query = search_query.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}&source=lnms&tbm=isch"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    image_urls = []
    for img in soup.find_all("img"):
        if "data-src" in img.attrs:
            image_url = img["data-src"]
        else:
            image_url = img["src"]
        image_urls.append(image_url)

    return image_urls[:num_images]

# 이미지 다운로드 예시
search_query = "dog hot spot img"
num_images = 100
image_urls = get_image_urls(search_query, num_images)

for i, url in enumerate(image_urls):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = f"image_{timestamp}_{i + 1}.jpg"
    download_image(url, file_path)
    print(f"다운로드 완료: {file_path}")

