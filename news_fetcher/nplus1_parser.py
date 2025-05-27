from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def fetch_news_selenium(limit=15):
    options = Options()
    options.add_argument("--headless")  # Запуск без окна браузера
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://nplus1.ru/news")
    
    time.sleep(5)  # Ждём, пока прогрузится JS

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Ищем заголовки новостей
    raw_cards = soup.select("a.n1_climb_4")
    news_items = []

    for card in raw_cards[:limit]:
        title = card.get_text(strip=True)
        link = card["href"]
        if not link.startswith("http"):
            link = "https://nplus1.ru" + link

        news_items.append({
            "title": title,
            "link": link
        })

    return news_items
