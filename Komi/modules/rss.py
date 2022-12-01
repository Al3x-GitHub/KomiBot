"""
MIT License

Copyright (c) 2022 ALEx

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

GitHub : https://github.com/Al3x-GitHub
"""
from asyncio import get_event_loop, sleep

from feedparser import parse
from pyrogram import filters
from pyrogram.types import Message

from Komi import RSS_DELAY, app
from Komi.core.decorators.errors import capture_err
from Komi.utils.dbfunctions import (
    add_rss_feed,
    get_rss_feeds,
    is_rss_active,
    remove_rss_feed,
    update_rss_feed,
)
from Komi.utils.functions import get_http_status_code, get_urls_from_text
from Komi.utils.rss import Feed

__MODULE__ = "RSS"
__HELP__ = f"""
/add_feed [URL] - Add a feed to chat
/rm_feed - Remove feed from chat

**Note:**
    - This will check for updates every {RSS_DELAY//60} minutes.
    - You can only add one feed per chat.
    - Currently RSS and ATOM feeds are supported.

© @MaximXRobot
"""


async def rss_worker():
    print("[INFO]: RSS WORKER STARTED")
    while True:
        feeds = await get_rss_feeds()
        if not feeds:
            await sleep(RSS_DELAY)
            continue

        loop = get_event_loop()

        for _feed in feeds:
            try:
                chat = _feed["chat_id"]
                url = _feed["url"]
                last_title = _feed.get("last_title")

                parsed = await loop.run_in_executor(None, parse, url)
                feed = Feed(parsed)

                if feed.title == last_title:
                    continue

                await app.send_message(
                    chat, feed.parsed(), disable_web_page_preview=True
                )
                await update_rss_feed(chat, feed.title)
            except Exception as e:
                print(str(e), f"RSS {chat}")
        await sleep(RSS_DELAY)


loop = get_event_loop()
loop.create_task(rss_worker())


@app.on_message(filters.command("add_feed"))
@capture_err
async def add_feed_func(_, m: Message):
    if len(m.command) != 2:
        return await m.reply("Read 'RSS' section in help menu.")
    url = m.text.split(None, 1)[1].strip()

    if not url:
        return await m.reply("[ERROR]: Invalid Argument")

    urls = get_urls_from_text(url)
    if not urls:
        return await m.reply("[ERROR]: Invalid URL")

    url = urls[0]
    status = await get_http_status_code(url)
    if status != 200:
        return await m.reply("[ERROR]: Invalid Url")

    ns = "[ERROR]: This feed isn't supported."
    try:
        loop = get_event_loop()
        parsed = await loop.run_in_executor(None, parse, url)
        feed = Feed(parsed)
    except Exception:
        return await m.reply(ns)
    if not feed:
        return await m.reply(ns)

    chat_id = m.chat.id
    if await is_rss_active(chat_id):
        return await m.reply("[ERROR]: You already have an RSS feed enabled.")
    try:
        await m.reply(feed.parsed(), disable_web_page_preview=True)
    except Exception:
        return await m.reply(ns)
    await add_rss_feed(chat_id, feed.url, feed.title)


@app.on_message(filters.command("rm_feed"))
async def rm_feed_func(_, m: Message):
    if await is_rss_active(m.chat.id):
        await remove_rss_feed(m.chat.id)
        await m.reply("Removed RSS Feed")
    else:
        await m.reply("There are no active RSS Feeds in this chat.")
