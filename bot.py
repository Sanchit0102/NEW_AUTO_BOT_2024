#(©) 𝚂𝙰𝙽𝙲𝙷𝙸𝚃 ♛⛧ 
import logging
import logging.config
import asyncio
import os
import time
import requests
from flask import Flask
from threading import Thread
from aiohttp import ClientSession
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from apscheduler.schedulers.background import BackgroundScheduler
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR, LOG_CHANNEL, PORT
from utils import temp
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from Script import script
from plugins import web_server

from aiohttp import web
from datetime import date, datetime 
import pytz

class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        logging.info(LOG_STR)
        logging.info(script.LOGO)
        tz = pytz.timezone('Asia/Kolkata')
        today = date.today()
        now = datetime.now(tz)
        time = now.strftime("%H:%M:%S %p")
        await self.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")

    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current + new_diff + 1)))
            for message in messages:
                yield message
                current += 1

# ===============[ RENDER PORT UPTIME ISSUE FIXED ]================ #

RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:5000")

app = Flask(__name__)

@app.route('/alive')
def alive():
    return "I am alive!"

def ping_self():
    url = f"{RENDER_EXTERNAL_URL}/alive"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info("Ping successful!")
        else:
            logging.error(f"Ping failed with status code {response.status_code}")
    except Exception as e:
        logging.error(f"Ping failed with exception: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler(timezone=pytz.utc)
    scheduler.add_job(ping_self, 'interval', minutes=3)
    scheduler.start()

def run_flask():
    app.run(host='0.0.0.0', port=10000)

Thread(target=run_flask).start()
start_scheduler()
app = Bot()
app.run()
