# celery_app.py

import sys
from celery import Celery
import os
from dotenv import load_dotenv
from datetime import timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

app = Celery('news_bot',
             broker='redis://redis:6379/0',
             backend='redis://redis:6379/0')

app.conf.timezone = 'Europe/Moscow'
logger.info("Current working directory: %s", os.getcwd())

from bot_sender.Telegram_send import send_telegram_message
from news_fetcher.nplus1_parser import fetch_news_selenium
from news_filter.filter_news_n import filter_news

# Configure the task to run every 30 seconds
app.conf.beat_schedule = {
    'fetch-and-send-news': {
        'task': 'celery_app.fetch_and_send_news',
        'schedule': timedelta(seconds=30),  # Run every 30 seconds
    },
}

@app.task
def fetch_and_send_news():
    positive_keywords = [
        "открытие",
        "достижение",
        "успех",
        "победа",
        "новинка",
        "обнаружили",
        "исследование",
        "учёные выяснили",
        "полезно",
        "совет",
        "как улучшить",
        "как стать",
        "улучшить",
        "продуктивность",
        "мотивация",
        "вдохновение",
        "невероятный",
        "удивительный",
        "факт",
        "интересно",
        "необычное",
        "лайфхак",
        "технология",
        "будущее",
        "прорыв",
        "рост",
        "развитие",
        "спокойствие",
        "радость",
        "улыбка",
        "добро",
        "позитив",
        "щедрость",
        "история успеха",
        "милое",
        "котик",
        "пёсик",
        "животные",
        "помощь",
        "волонтёр",
        "дети помогли",
        "чудо",
        "спасли",
        "счастье",
        "отдых",
        "гармония",
        "здоровье",
        "психология",
        "благополучие",
        "саморазвитие",
        "навык",
        "простое решение",
        "удалось",
        "нашли способ",
        "инновация",
        "новый подход",
        "улучшения",
        "экологично",
        "эко",
        "умное",
        "автоматизация",
        "простой способ",
        "оптимизация",
        "успешный",
        "перемены к лучшему",
        "решение найдено",
        "положительное",
        "неожиданно приятно",
        "праздник",
        "юбилей",
        "рекорд",
        "хобби",
        "творчество",
        "вдохновляющая история",
        "самое лучшее",
        "рекомендации",
        "на заметку",
        "тёплая история",
        "любовь",
        "доброта",
    ]
    
    negative_keywords = [
        "убийство",
        "смерть",
        "погиб",
        "погибли",
        "умер",
        "умерла",
        "погибла",
        "авария",
        "катастрофа",
        "трагедия",
        "взрыв",
        "взорвался",
        "застрелил",
        "нападение",
        "изнасилование",
        "жестокость",
        "насилие",
        "жертва",
        "криминал",
        "расследование",
        "арест",
        "суд",
        "штраф",
        "приговор",
        "тюрьма",
        "полиция",
        "ограбление",
        "драка",
        "конфликт",
        "скандал",
        "сенсация",
        "обман",
        "мошенник",
        "кража",
        "вор",
        "похищение",
        "терроризм",
        "теракт",
        "угроза",
        "паника",
        "кризис",
        "рецессия",
        "инфляция",
        "банкротство",
        "война",
        "вторжение",
        "бомбардировка",
        "фронт",
        "армия",
        "военные",
        "вооружённый",
        "политика",
        "политик",
        "правительство",
        "президент",
        "депутат",
        "выборы",
        "партия",
        "санкции",
        "коррупция",
        "оппозиция",
        "митинг",
        "протест",
        "цензура",
        "репрессии",
        "болезнь",
        "вирус",
        "пандемия",
        "ковид",
        "грипп",
        "заражение",
        "эпидемия",
        "рак",
        "инфекция",
        "диагноз",
        "больница",
        "реанимация",
        "страдание",
        "инвалидность",
        "депрессия",
        "паническая атака",
        "стресс",
        "боль",
        "слёзы",
        "развод",
        "измена",
        "разрыв",
        "самоубийство",
        "звезда",
        "селебрити",
        "шоу-бизнес",
        "гламур",
        "интрига",
        "сплетни",
        "оскар",
        "разоблачение",
        "шок",
        "ужас",
        "страшно",
        "отвратительно",
        "невыносимо",
        "грязь",
        "виновен",
        "обвинили",
        "стыд",
        "ненависть",
    ]
    
    try:
        # Fetch news
        all_news = fetch_news_selenium()
        logger.info(f"Total news found: {len(all_news)}")
        
        # Filter news
        filtered = filter_news(all_news, positive_keywords, negative_keywords)
        logger.info(f"Filtered news count: {len(filtered)}")
        
        # Send to Telegram
        successful_sends = 0
        for news in filtered:
            message = f"<b>{news['title']}</b>\n{news['link']}"
            response = send_telegram_message(message)
            
            if response.get('ok'):
                successful_sends += 1
                logger.info(f"Successfully sent: {news['title']}")
            else:
                logger.error(f"Failed to send news. Title: {news['title']}, Error: {response.get('error') or response}")
            
        result_msg = f"Successfully sent {successful_sends} out of {len(filtered)} news items"
        logger.info(result_msg)
        return result_msg
        
    except Exception as e:
        error_msg = f"Error in fetch_and_send_news task: {str(e)}"
        logger.error(error_msg)
        return error_msg