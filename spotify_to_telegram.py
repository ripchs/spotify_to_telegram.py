import os
import asyncio
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from telegram import Bot
from telegram.ext import Application

# 🔑 Вставь сюда свои данные:
SPOTIFY_CLIENT_ID = "0a038fc36d8d4aa4922cb33991f0754a"
SPOTIFY_CLIENT_SECRET = "c71c80c2642045b585bc9b2777417472"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
TELEGRAM_TOKEN = "8069908850:AAEehMGaCCEK1zAqvmrt-SD7oP8AkdyqJGk"
TELEGRAM_CHAT_ID = "1248516794"

# 🎧 Авторизация Spotify
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-playback-state"
)
sp = Spotify(auth_manager=sp_oauth)

# 🔍 Получаем текущий трек
current = sp.current_playback()
print("Spotify ответ:", current)

# ✉️ Готовим сообщение
if current and current.get('is_playing'):
    track = current['item']
    track_name = track['name']
    artist_name = ', '.join([artist['name'] for artist in track['artists']])
    message = f"🎵 Сейчас играет: {track_name} — {artist_name}"
else:
    message = "⏸ Сейчас ничего не играет"

# 📤 Асинхронная отправка в Telegram
async def send_message():
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    print("✅ Сообщение отправлено!")

# Запускаем асинхронную задачу
asyncio.run(send_message())
