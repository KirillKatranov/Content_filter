KEYWORDS = ["ИИ", "робот", "физика", "дрон", "квант"]

def filter_news(news_list, positive_keywords, negative_keywords):
    filtered = []
    for item in news_list:
        title_lower = item["title"].lower()

        has_positive = any(kw.lower() in title_lower for kw in positive_keywords)
        has_negative = any(kw.lower() in title_lower for kw in negative_keywords)

        if has_positive and not has_negative:
            filtered.append(item)

    return filtered

