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

from Komi import app
from Komi.core.decorators.errors import capture_err
from Komi.utils.http import get, resp_get

__MODULE__ = "Cats"
__HELP__ = """/randomcat - To Get Random Photo of Cat.
/catfacts - To Get Facts About Cat.

© @MaximXRobot
"""


@app.on_message(filters.command("randomcat"))
@capture_err
async def randomcat(_, message):
    cat = await get("https://aws.random.cat/meow")
    await message.reply_photo(cat.get("file"))
