# News Filter Bot

This project fetches news from specified sources, filters them based on positive and negative keywords, and sends the filtered news to a Telegram bot. The application is containerized using Docker and uses Celery for scheduled tasks.

## Prerequisites

- Docker
- Docker Compose
- Telegram Bot Token
- Telegram Chat ID

## Setup

1. Create a `.env` file in the root directory with the following content:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

2. Replace `your_bot_token_here` with your Telegram bot token
3. Replace `your_chat_id_here` with your Telegram chat ID

## Running the Application

1. Build and start the containers:
```bash
docker-compose up --build
```

This will start:
- Redis service
- Celery worker
- Celery beat scheduler

The application will automatically:
- Fetch news at 9:00 AM daily
- Filter the news based on configured keywords
- Send filtered news to the specified Telegram chat

## Services

- **Redis**: Message broker for Celery
- **Celery Worker**: Processes the news fetching and filtering tasks
- **Celery Beat**: Schedules the daily news fetching task

## Monitoring

You can monitor the logs using:
```bash
docker-compose logs -f
```

## Stopping the Application

To stop all services:
```bash
docker-compose down
``` 