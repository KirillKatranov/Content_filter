from celery_app import celery
from news_fetcher.nplus1_parser import fetch_news_selenium
from news_filter.filter_news_n import filter_news
from bot_sender.Telegram_send import send_telegram_message

@celery.task
def send_filtered_news():
    all_news = fetch_news_selenium()
    keywords = ["ИИ", "дрон", "квант", "робот"]
    filtered = filter_news(all_news, keywords)

    for item in filtered:
        msg = f"<b>{item['title']}</b>\n{item['link']}"
        send_telegram_message(msg)