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
from pyrogram import filters
from pyrogram.types import Message

from Komi import SUDOERS, app, arq
from Komi.utils.filter_groups import autocorrect_group


@app.on_message(filters.command("autocorrect"))
async def autocorrect_bot(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a text message.")
    reply = message.reply_to_message
    text = reply.text or reply.caption
    if not text:
        return await message.reply_text("Reply to a text message.")
    data = await arq.spellcheck(text)
    if not data.ok:
        return await message.reply_text("Something wrong happened.")
    result = data.result
    await message.reply_text(result.corrected or "Empty")
