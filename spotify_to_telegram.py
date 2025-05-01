import os
from flask import Flask
import asyncio
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import telegram

app = Flask(__name__)

# Настройки
SPOTIFY_CLIENT_ID = "0a038fc36d8d4aa4922cb33991f0754a"
SPOTIFY_CLIENT_SECRET = "c71c80c2642045b585bc9b2777417472"
SPOTIFY_REDIRECT_URI = "https://your-app-name.up.railway.app/callback"  # Новая ссылка
TELEGRAM_TOKEN = "8069908850:AAEehMGaCCEK1zAqvmrt-SD7oP8AkdyqJGk"
TELEGRAM_CHAT_ID = "1248516794"

# Авторизация Spotify
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-playback-state"
)
sp = Spotify(auth_manager=sp_oauth)

@app.route('/')
def home():
    current = sp.current_playback()
    if current and current.get('is_playing'):
        track = current['item']
        track_name = track['name']
        artist_name = ', '.join([artist['name'] for artist in track['artists']])
        message = f"🎵 Сейчас играет: {track_name} — {artist_name}"
    else:
        message = "⏸ Сейчас ничего не играет"

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    return "Сообщение отправлено!"

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Railway автоматически назначает порт
    app.run(host="0.0.0.0", port=port)  # Запускаем сервер на Railway
