import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime

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
    # 검색어를 URL 인코딩하여 검색 쿼리 생성
    query = search_query.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}&source=lnms&tbm=isch"

    # User-Agent 설정 (크롬 브라우저 User-Agent)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # HTTP GET 요청
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # HTML 파싱
    soup = BeautifulSoup(response.text, "html.parser")

    # 이미지 URL 추출
    image_urls = []
    for img in soup.find_all("img"):
        image_urls.append(img["src"])

    return image_urls[:num_images]

# 이미지 다운로드 예시
search_query = "dog ring worm "
num_images = 100
image_urls = get_image_urls(search_query, num_images)

for i, url in enumerate(image_urls):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # 현재 시간 정보
    file_path = f"image_{timestamp}_{i + 1}.jpg"
    download_image(url, file_path)
    print(f"다운로드 완료: {file_path}")
