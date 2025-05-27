from news_fetcher.nplus1_parser import fetch_news_selenium

if __name__ == "__main__":
    news = fetch_news_selenium()
    for item in news:
        print(f"{item['title']}\n{item['link']}\n")
