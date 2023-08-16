import requests
import pandas as pd
import time
import math
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 불러오기
load_dotenv()


# API endpoint URL
url = "https://tasty.p.rapidapi.com/recipes/list"

# headers는 API 요청에 필요한 인증 정보를 담고 있습니다.
headers = {
    "X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"],
    "X-RapidAPI-Host": "tasty.p.rapidapi.com",
}

# 비어있는 DataFrame 생성
df = pd.DataFrame()

# 조회할 데이터의 개수와 크기를 설정합니다.
size = 40
target_count = 500

# math.ceil 함수를 사용하여 반복 횟수를 계산합니다.
number_of_calls = math.ceil(target_count / size)

# for문으로 API 호출을 반복합니다. (전체 요청이 완료될 때까지)
for call_index in range(number_of_calls):
    # 'from' 값 계산
    from_value = call_index * size

    # Querystring에 'from'과 'size'를 추가하여 설정합니다.
    querystring = {"from": str(from_value), "size": str(size)}

    # API 요청을 실행합니다.
    response = requests.get(url, headers=headers, params=querystring)

    # JSON 결과를 파싱합니다.
    result = response.json()

    # 결과 중 "results"를 가져옵니다.
    data_list = result["results"]

    # 결과를 DataFrame으로 변환합니다.
    temp_df = pd.DataFrame(data_list)

    # 결과를 주 DataFrame에 추가합니다.
    df = pd.concat([df, temp_df], ignore_index=True, axis=0)

    # API 호출 사이에 딜레이를 추가합니다 (예: 0.1초).
    time.sleep(0.1)

# 최종 DataFrame을 JSON 파일로 저장합니다.
df.to_json(
    "C:/dev_course/25. 4차_플젝/data/test_api.json", orient="records", force_ascii=False
)


# 한 번에 40개
# 총 count: 9731
