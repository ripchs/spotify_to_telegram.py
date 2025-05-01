import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import telebot

# Токены и настройки
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Авторизация в Spotify
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-playback-state"
)

sp = spotipy.Spotify(auth_manager=sp_oauth)

# Получение информации о текущем воспроизведении
current = sp.current_playback()

# Проверка, если песня играет
if current and current.get('is_playing'):
    track = current['item']
    track_name = track['name']
    artist_name = ', '.join([artist['name'] for artist in track['artists']])
    message = f"🎵 Сейчас играет: {track_name} — {artist_name}"
else:
    message = "⏸ Сейчас ничего не играет"

# Отправка сообщения в Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)
bot.send_message(TELEGRAM_CHAT_ID, message)

print("Сообщение отправлено!")
