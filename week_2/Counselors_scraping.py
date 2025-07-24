from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd

options = Options()
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

url = "https://trost.co.kr/service/search/partner/"
driver.get(url)
time.sleep(3)

results = []

def extract_price(price_tag):
    if price_tag:
        text = price_tag.text.strip().replace(",", "").replace("원", "")
        return int(text) if text.isdigit() else "N/A"
    return "N/A"

def scrape_current_page():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    panel = soup.select_one("#partnerSearchListPanel")

    cards = panel.select("article.partner-list-box")
    for card in cards:
        name_tag = card.select_one("div.partner-list-box__info.js-partner-list-box__info > h3")
        if name_tag:
            name = name_tag.text.strip().replace("NEW", "").strip()
        else:
            name = "N/A"

        text_price_tag = card.select_one("div.counseling-type__texttime > div")
        tel_price_tag = card.select_one("div.counseling-type__voicetime > div")
        off_price_tag=card.select_one("div.counseling-type__offlinetime > div")
        text_price = extract_price(text_price_tag)
        tel_price = extract_price(tel_price_tag)
        off_price = extract_price(off_price_tag)

        review_tag = card.select_one("div.partner-list-box__review-score.js-review-star-num")
        review = review_tag.text.strip()[1:-1] if review_tag else "N/A"

        tagline_tag = card.select_one(
            "div.partner-list-box__info.js-partner-list-box__info > div > div.partner-item__keyword-list")
        tagline = tagline_tag.text.strip() if tagline_tag else "N/A"

        message_tag = card.select_one("div > div.partner-list-box__marketing-message")
        message = message_tag.text.strip() if message_tag else "N/A"

        star_tags = card.select("div.star-score__wrap--middle li")
        full_stars = sum(1 for li in star_tags if "is-all" in li.get("class", []))
        half_stars = sum(1 for li in star_tags if "is-half" in li.get("class", []))
        rating = full_stars + 0.5 * half_stars

        print(f"이름: {name}")
        print(f"키워드: {tagline}")
        print(f"소개: {message}")
        print(f"⭐ 별점: {rating} / 5.0")
        print(f"리뷰수: {review}")
        print(f"가격: {tel_price}/{text_price}/{off_price}")
        print("-" * 40)

        results.append({
            "name": name,
            "review_count": review,
            "phone_price": tel_price,
            "text_price": text_price,
            "offline_price": off_price,
            "keywords": tagline,
            "summary": message,
            "rating": rating
        })

for i in range(1, 6):
    if i > 1:
        try:
            page_btns = driver.find_elements("css selector", "li.js-list__pagination--num a")
            for btn in page_btns:
                if btn.text.strip() == str(i):
                    btn.click()
                    time.sleep(2)
                    break
        except Exception as e:
            print(f"{i}페이지 이동 실패: {e}")
            break

    print(f"===== Page {i} =====")
    scrape_current_page()

driver.quit()

df = pd.DataFrame(results)
df.to_csv("trost_counselors.csv", index=False)