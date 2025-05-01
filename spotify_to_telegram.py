import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from telegram import Bot

# Укажи здесь свои данные:
SPOTIFY_CLIENT_ID = '0a038fc36d8d4aa4922cb33991f0754a'
SPOTIFY_CLIENT_SECRET = 'c01617b287f5430191fdeac8b83c6bbb'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'
TELEGRAM_TOKEN = '8069908850:AAEehMGaCCEK1zAqvmrt-SD7oP8AkdyqJGk'
TELEGRAM_CHAT_ID = '1248516794'  # об этом ниже

# Авторизация в Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-currently-playing"
))

# Авторизация в Telegram
bot = Bot(token=TELEGRAM_TOKEN)

last_track = None

while True:
    try:
        current = sp.current_user_playing_track()
        if current and current['is_playing']:
            track = current['item']['name']
            artist = current['item']['artists'][0]['name']
            url = current['item']['external_urls']['spotify']

            message = f"Сейчас играет: {track} — {artist}\n{url}"

            if message != last_track:
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
                last_track = message

    except Exception as e:
        print(f"Ошибка: {e}")

    time.sleep(30)  # Проверка каждые 30 секунд
