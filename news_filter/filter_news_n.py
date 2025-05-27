KEYWORDS = ["ИИ", "робот", "физика", "дрон", "квант"]

def filter_news(news_list, keywords):
    filtered = []
    for item in news_list:
        title_lower = item["title"].lower()
        if any(kw.lower() in title_lower for kw in keywords):
            filtered.append(item)
    return filtered
