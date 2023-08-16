import requests
import pandas as pd
from xml.etree import ElementTree
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 불러오기
load_dotenv()

# api_key = "xxxxxxxxxxxxx"
api_key = os.environ["MINISTRY_FOOD_API_KEY"]

start_index = 1
total_data_count = 1000
items_per_request = 1000

data = []
columns = [
    "RCP_SEQ",
    "RCP_NM",
    "RCP_PARTS_DTLS",
    "INFO_WGT",
    "RCP_WAY2",
    "RCP_PAT2",
    "ATT_FILE_NO_MAIN",
    "ATT_FILE_NO_MK",
    "MANUAL01",
    "MANUAL02",
    "MANUAL03",
    "MANUAL04",
    "MANUAL05",
    "MANUAL06",
    "MANUAL07",
    "MANUAL08",
    "MANUAL09",
    "MANUAL10",
    "MANUAL11",
    "MANUAL12",
    "MANUAL13",
    "MANUAL14",
    "MANUAL15",
    "MANUAL16",
    "MANUAL17",
    "MANUAL18",
    "MANUAL19",
    "MANUAL20",
    "MANUAL_IMG01",
    "MANUAL_IMG02",
    "MANUAL_IMG03",
    "MANUAL_IMG04",
    "MANUAL_IMG05",
    "MANUAL_IMG06",
    "MANUAL_IMG07",
    "MANUAL_IMG08",
    "MANUAL_IMG09",
    "MANUAL_IMG10",
    "MANUAL_IMG11",
    "MANUAL_IMG12",
    "MANUAL_IMG13",
    "MANUAL_IMG14",
    "MANUAL_IMG15",
    "MANUAL_IMG16",
    "MANUAL_IMG17",
    "MANUAL_IMG18",
    "MANUAL_IMG19",
    "MANUAL_IMG20",
]

new_column_names = {
    "RCP_SEQ": "API_ID",
    "RCP_NM": "food_name",
    "RCP_PARTS_DTLS": "ingredient",
    "INFO_WGT": "serving",
    "RCP_WAY2": "category",
    "RCP_PAT2": "category_2",
    "ATT_FILE_NO_MAIN": "food_img_1",
    "ATT_FILE_NO_MK": "food_img_2",
    "MANUAL01": "recipe_01",
    "MANUAL02": "recipe_02",
    "MANUAL03": "recipe_03",
    "MANUAL04": "recipe_04",
    "MANUAL05": "recipe_05",
    "MANUAL06": "recipe_06",
    "MANUAL07": "recipe_07",
    "MANUAL08": "recipe_08",
    "MANUAL09": "recipe_09",
    "MANUAL10": "recipe_10",
    "MANUAL11": "recipe_11",
    "MANUAL12": "recipe_12",
    "MANUAL13": "recipe_13",
    "MANUAL14": "recipe_14",
    "MANUAL15": "recipe_15",
    "MANUAL16": "recipe_16",
    "MANUAL17": "recipe_17",
    "MANUAL18": "recipe_18",
    "MANUAL19": "recipe_19",
    "MANUAL20": "recipe_20",
    "MANUAL_IMG01": "recipe_img_01",
    "MANUAL_IMG02": "recipe_img_02",
    "MANUAL_IMG03": "recipe_img_03",
    "MANUAL_IMG04": "recipe_img_04",
    "MANUAL_IMG05": "recipe_img_05",
    "MANUAL_IMG06": "recipe_img_06",
    "MANUAL_IMG07": "recipe_img_07",
    "MANUAL_IMG08": "recipe_img_08",
    "MANUAL_IMG09": "recipe_img_09",
    "MANUAL_IMG10": "recipe_img_10",
    "MANUAL_IMG11": "recipe_img_11",
    "MANUAL_IMG12": "recipe_img_12",
    "MANUAL_IMG13": "recipe_img_13",
    "MANUAL_IMG14": "recipe_img_14",
    "MANUAL_IMG15": "recipe_img_15",
    "MANUAL_IMG16": "recipe_img_16",
    "MANUAL_IMG17": "recipe_img_17",
    "MANUAL_IMG18": "recipe_img_18",
    "MANUAL_IMG19": "recipe_img_19",
    "MANUAL_IMG20": "recipe_img_20",
}


while start_index <= total_data_count:
    end_index = start_index + items_per_request - 1
    if end_index > total_data_count:
        end_index = total_data_count

    url = f"http://openapi.foodsafetykorea.go.kr/api/{api_key}/COOKRCP01/xml/{start_index}/{end_index}"
    response = requests.get(url)

    if response.status_code == 200:
        tree = ElementTree.fromstring(response.content)
        rows = tree.findall("row")

        for row in rows:
            row_data = [
                row.find(col).text if row.find(col) is not None else ""
                for col in columns
            ]
            data.append(row_data)

    else:
        print("API 호출 실패:", response.status_code)
        break

    start_index += items_per_request


df = pd.DataFrame(data, columns=columns)
df = df.rename(columns=new_column_names)
df = df.drop(
    [
        "recipe_07",
        "recipe_08",
        "recipe_09",
        "recipe_10",
        "recipe_11",
        "recipe_12",
        "recipe_13",
        "recipe_14",
        "recipe_15",
        "recipe_16",
        "recipe_17",
        "recipe_18",
        "recipe_19",
        "recipe_20",
        "recipe_img_07",
        "recipe_img_08",
        "recipe_img_09",
        "recipe_img_10",
        "recipe_img_11",
        "recipe_img_12",
        "recipe_img_13",
        "recipe_img_14",
        "recipe_img_15",
        "recipe_img_16",
        "recipe_img_17",
        "recipe_img_18",
        "recipe_img_19",
        "recipe_img_20",
    ],
    axis=1,
)

df["serving"] = "1인분"

# 원래 컬럼에서 "[숫자인분]" 패턴 제거
df["ingredient"] = df["ingredient"].str.replace("(\[\d+인분\])", "", regex=True)
df["ingredient"] = df["ingredient"].str.replace("(\[\s*\d+인분\s*\])", "", regex=True)


row_count = df.shape[0]
print("행 개수: ", row_count)


df.to_csv("C:/dev_course/25. 4차_플젝/data/data.csv", encoding="utf-8-sig", index=False)

df.to_json("C:/dev_course/25. 4차_플젝/data/api.json", orient="records", force_ascii=False)


"""
df.to_parquet(
    "C:/dev_course/25. 4차_플젝/data/data.parquet",
    engine="pyarrow",
    compression="snappy",
)
"""
