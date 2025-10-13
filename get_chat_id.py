import requests

TOKEN = "7897180848:AAHbubHEOfvy-F2YqR3k1HuZLvzInxL-9tA"
URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

response = requests.get(URL)
data = response.json()
print(data)