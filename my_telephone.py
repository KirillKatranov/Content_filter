import os
import logging
import asyncio
from pathlib import Path
from telethon import TelegramClient, errors
from telethon.sessions import SQLiteSession
from sqlite3 import DatabaseError

# ===========  КОНФИГ  ===========
API_ID   = int(os.getenv('TELEGRAM_API_ID', '123456'))
API_HASH = os.getenv('TELEGRAM_API_HASH', 'abcdef0123456789')
SESSION_NAME = 'my_telegram'                     # базовое имя сессии

# Папка для хранения сессий рядом со скриптом
BASE_DIR    = Path(__file__).parent.resolve()
SESSION_DIR = BASE_DIR / 'sessions'
SESSION_DIR.mkdir(exist_ok=True)
# НЕ ДОБАВЛЯЕМ .session — Telethon сам добавит его
SESSION_PATH = SESSION_DIR / SESSION_NAME

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.INFO
)


async def main():
    # создаём клиент, телега сама создаст ./sessions/my_telegram.session
    client = TelegramClient(str(SESSION_PATH), API_ID, API_HASH)
    
    await client.connect()
    
    # если ещё не авторизованы — логинимся
    if not await client.is_user_authorized():
        phone = input('📱 Введите номер телефона (+7…): ')
        try:
            await client.send_code_request(phone)
        except errors.PhoneNumberBannedError:
            logging.error('❌ Этот номер заблокирован в Telegram, код не отправить.')
            return
        except errors.FloodWaitError as e:
            logging.error(f'⏳ Нужно подождать {e.seconds} секунд перед кодом.')
            return

        code = input('📨 Введите код из Telegram: ')
        try:
            await client.sign_in(phone, code)
        except errors.SessionPasswordNeededError:
            # 2FA
            pwd = input('🔒 Введите 2FA-пароль: ')
            try:
                await client.sign_in(password=pwd)
            except Exception as e:
                logging.error(f'❌ Не удалось пройти 2FA: {e}')
                return
        except errors.PhoneCodeInvalidError:
            logging.error('❌ Неверный код подтверждения.')
            return
        except errors.PhoneCodeExpiredError:
            logging.error('❌ Код истёк, запросите заново.')
            return
        except Exception as e:
            logging.error(f'❌ Ошибка при входе: {e}')
            return

        logging.info('✅ Авторизация прошла успешно!')

    else:
        logging.info('👍 Используем существующую сессию — не запрашиваем телефон.')

    me = await client.get_me()
    logging.info(f'Авторизованы как: {me.first_name} (ID={me.id})')

    # … ваша логика …
    # пример: 3 последних сообщения из @example
    async for msg in client.iter_messages('example', limit=3):
        date = msg.date.strftime('%Y-%m-%d %H:%M')
        text = msg.text or '<медиа>'
        print(f'[{date}] {msg.sender_id}: {text}')

    await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())