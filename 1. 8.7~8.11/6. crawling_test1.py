from bs4 import BeautifulSoup
import re

html = """
<div class="wrap">
    <div id="content"><div id="column1" style="height:100%"><div id="login" class="global_box">                        
        <div style="padding-bottom:20px;border-bottom:1px solid #aaa;" class="bbs_list_header"><div class="btit-s10"></div><h1>히트레시피</h1><h2>더이상의 레시피는 없다, 검증된 레시피 모음</h2><div style="width:332px;top:0px;right:0px;position:absolute;"></div>
        </div><div id="readTitle" style="background:#eee;padding:10px;margin-bottom:10px;border:1px solid #ddd;">
          <h2 class="readTitle">당근 라페 (당근채절임)</h2>
          작성자 : <strong class="user_profile user_function"><a rel="12003">82cook</a></strong> |
          조회수 : 51,973  |
          추천수 : <span id="boom">0</span>
          <div class="regdate">작성일 : 2021-07-10 19:26:25</div>
        </div>
    </div></div></div>
"""

soup = BeautifulSoup(html, "html.parser")

recipe_name = soup.find("h2", {"class": "readTitle"}).text.strip()

info_text = soup.find("div", class_="regdate").previous_sibling.strip()

views = re.findall("조회수 : *([0-9,]+)", info_text)
views = int(views[0].replace(",", ""))

recommendations = re.findall('추천수 : *<span id="boom">([0-9,]+)<\/span>', info_text)
recommendations = int(recommendations[0].replace(",", ""))

print(f"요리 이름: {recipe_name}")
print(f"조회수: {views}")
print(f"추천수: {recommendations}")
