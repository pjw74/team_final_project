import requests
from bs4 import BeautifulSoup
import json

url = "https://www.youtube.com/watch?v=w9ML-v8OG1Y&list=PLoABXt5mipg6mIdGKBuJlv5tmQFAQ3OYr&index=6"

# 해당 웹페이지 가져오기
response = requests.get(url)

# 상태 코드가 200(정상 응답)인 경우에만 BeautifulSoup 객체를 생성하고 정보를 추출
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # 원하는 정보 출력 (영상 데이터)
    video_data_tag = soup.find(
        "script", {"id": "scriptTag", "type": "application/ld+json"}
    )

    if video_data_tag:
        video_data_json = json.loads(video_data_tag.string)
        description = video_data_json["description"]

        # 영상 설명 출력
        print("영상 설명:", description.strip())
    else:
        print("영상 설명을 찾을 수 없습니다.")
else:
    print("웹페이지를 가져오지 못했습니다. 상태 코드:", response.status_code)
