#(©) 𝚂𝙰𝙽𝙲𝙷𝙸𝚃 ♛⛧ 
import logging
import logging.config

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR, LOG_CHANNEL, PORT
from utils import temp
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from Script import script
from plugins import web_server
from aiohttp import web
from datetime import date, datetime 

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
        asyncio.create_task(self.keep_alive()) 
        
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

    async def keep_alive(self):
        keep_alive_url = "https://new-auto-bot-2024-jke2.onrender.com"  # Replace with your keep-alive URL
        interval = 5 * 60  # Ping every 25 minutes

        async with ClientSession() as session:
            while True:
                try:
                    async with session.get(keep_alive_url) as response:
                        if response.status == 200:
                            logging.info("Keep-alive ping successful.")
                        else:
                            logging.warning(f"Keep-alive ping failed with status: {response.status}")
                except Exception as e:
                    logging.error(f"Keep-alive ping failed: {e}")
                await asyncio.sleep(interval)


app = Bot()
app.run()
# import sys
# import glob
# import importlib
# from pathlib import Path
# from pyrogram import idle
# import logging
# import logging.config

# # Get logging configurations
# logging.config.fileConfig('logging.conf')
# logging.getLogger().setLevel(logging.INFO)
# logging.getLogger("pyrogram").setLevel(logging.ERROR)
# logging.getLogger("imdbpy").setLevel(logging.ERROR)
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
# logging.getLogger("aiohttp").setLevel(logging.ERROR)
# logging.getLogger("aiohttp.web").setLevel(logging.ERROR)


# from pyrogram import Client, __version__
# from pyrogram.raw.all import layer
# from database.ia_filterdb import Media
# from database.users_chats_db import db
# from info import *
# from utils import temp
# from typing import Union, Optional, AsyncGenerator
# from pyrogram import types
# from Script import script 
# from aiohttp import web

# # import asyncio
# # from pyrogram import idle
# # from lazybot import LazyPrincessBot
# # from util.keepalive import ping_server
# # from lazybot.clients import initialize_clients


# ppath = "plugins/*.py"
# files = glob.glob(ppath)
# LazyPrincessBot.start()
# loop = asyncio.get_event_loop()


# async def Lazy_start():
#     print('\n')
#     print('Initalizing Lazy Bot')
#     bot_info = await LazyPrincessBot.get_me()
#     LazyPrincessBot.username = bot_info.username
#     await initialize_clients()
#     for name in files:
#         with open(name) as a:
#             patt = Path(a.name)
#             plugin_name = patt.stem.replace(".py", "")
#             plugins_dir = Path(f"plugins/{plugin_name}.py")
#             import_path = "plugins.{}".format(plugin_name)
#             spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
#             load = importlib.util.module_from_spec(spec)
#             spec.loader.exec_module(load)
#             sys.modules["plugins." + plugin_name] = load
#             print("Lazy Imported => " + plugin_name)
#     if ON_HEROKU:
#         asyncio.create_task(ping_server())
#     b_users, b_chats = await db.get_banned()
#     temp.BANNED_USERS = b_users
#     temp.BANNED_CHATS = b_chats
#     await Media.ensure_indexes()
#     me = await LazyPrincessBot.get_me()
#     temp.ME = me.id
#     temp.U_NAME = me.username
#     temp.B_NAME = me.first_name
#     LazyPrincessBot.username = '@' + me.username
#     logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
#     logging.info(LOG_STR)
#     logging.info(script.LOGO)
#     tz = pytz.timezone('Asia/Kolkata')
#     today = date.today()
#     now = datetime.now(tz)
#     time = now.strftime("%H:%M:%S %p")
#     await LazyPrincessBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
#     app = web.AppRunner(await web_server())
#     await app.setup()
#     bind_address = "0.0.0.0"
#     await web.TCPSite(app, bind_address, PORT).start()
#     await idle()


# if __name__ == '__main__':
#     try:
#         loop.run_until_complete(Lazy_start())
#     except KeyboardInterrupt:
#         logging.info('Service Stopped Bye 👋')
