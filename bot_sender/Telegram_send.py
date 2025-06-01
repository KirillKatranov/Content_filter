import requests
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(text):
    if not TOKEN:
        logger.error("Telegram bot token is not set!")
        return {"error": "Bot token not configured"}
    
    if not CHAT_ID:
        logger.error("Telegram chat ID is not set!")
        return {"error": "Chat ID not configured"}

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    
    try:
        logger.info(f"Sending message to Telegram chat {CHAT_ID}")
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        result = response.json()
        
        if response.status_code == 200 and result.get('ok'):
            logger.info("Message sent successfully")
            return result
        else:
            logger.error(f"Failed to send message. Response: {result}")
            return result
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Error sending message to Telegram: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}
