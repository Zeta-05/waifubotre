class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "6558846590"
    sudo_users = "6558846590"
    GROUP_ID = -1001926606886
    TOKEN = "6574068893:AAHAFpK9STkslWOMY94kR-6kJinSi6FEhWo"
    mongo_url = "mongodb+srv://yunyxedits:assalom%4013@waifudata.vfutysm.mongodb.net/?retryWrites=true&w=majority&appName=waifudata"
    PHOTO_URL = ["https://ibb.co/q7jzMwz", "https://ibb.co/T2qNx5m", "https://ibb.co/TYS7yC4", "https://ibb.co/hVRR0T1", "https://ibb.co/3W3rVy6"]
    SUPPORT_CHAT = "Aniverse_Group"
    UPDATE_CHAT = "Aniverse_Updates"
    BOT_USERNAME = "AniverseWaifuBot"
    CHARA_CHANNEL_ID = "-1001926606886"
    api_id = 24698455
    api_hash = "00d4cd57b1fb369ea65563d40c9c2494"

    STRICT_GBAN = True
    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
