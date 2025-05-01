
import os
import asyncio
from aiohttp import web
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from telegram import Bot

# Получаем переменные окружения
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

async def send_current_track():
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="user-read-playback-state"
    )
    sp = Spotify(auth_manager=sp_oauth)
    current = sp.current_playback()

    if current and current.get('is_playing'):
        track = current['item']
        name = track['name']
        artists = ', '.join([a['name'] for a in track['artists']])
        msg = f"🎵 Сейчас играет: {name} — {artists}"
    else:
        msg = "⏸ Сейчас ничего не играет"

    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

async def handle(request):
    await send_current_track()
    return web.Response(text="✅ Отправлено в Telegram")

app = web.Application()
app.router.add_get("/", handle)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    web.run_app(app, port=port)
