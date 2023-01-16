from os import environ, path

from dotenv import load_dotenv

if path.exists("config.env"):
    load_dotenv("config.env")

BOT_TOKEN = environ.get("5859358588:AAEL0muib9YFVc8I9L6M9k3HhhWTWo1alYI", 5859358588:AAEL0muib9YFVc8I9L6M9k3HhhWTWo1alYI)
API_ID = int(environ.get("API_ID", 12738003))
API_HASH = environ.get("API_HASH", "b00dd4adc30230fcd86dde58f5dee5d0")
SUDO_USERS_ID = [int(x) for x in environ.get("SUDO_USERS_ID", "").split()]
LOG_GROUP_ID = int(environ.get("LOG_GROUP_ID", -1001501356475))
GBAN_LOG_GROUP_ID = int(environ.get("GBAN_LOG_GROUP_ID", None))
MESSAGE_DUMP_CHAT = int(environ.get("MESSAGE_DUMP_CHAT", None))
WELCOME_DELAY_KICK_SEC = int(environ.get("WELCOME_DELAY_KICK_SEC", None))
MONGO_URL = environ.get("MONGO_URL", mongodb+srv://Izumi:174029@cluster0.juphmfi.mongodb.net/?retryWrites=true&w=majority)
ARQ_API_URL = environ.get("ARQ_API_URL", None)
ARQ_API_KEY = environ.get("ARQ_API_KEY", None)
RSS_DELAY = int(environ.get("RSS_DELAY", None))
UPSTREAM_REPO = environ.get(
    "UPSTREAM_REPO", "https://github.com/Al3x-GitHub/KomiBot.git"
)
