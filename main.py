from bot_sender.Telegram_send import send_telegram_message
from news_fetcher.nplus1_parser import fetch_news_selenium
from news_filter.filter_news_n import filter_news  

if __name__ == "__main__":
    all_news = fetch_news_selenium()
    print(f"Всего найдено: {len(all_news)}")

    keywords = ["ИИ", "робот", "физика", "дрон"]
    filtered = filter_news(all_news, keywords)

    print(f"Подходящие новости: {len(filtered)}\n")
    for news in filtered:
        message = f"<b>{news['title']}</b>\n{news['link']}"
        send_telegram_message(message)
        print(f"{news['title']}\n{news['link']}\n")
