from telegram import Update, ChatMemberUpdated
from telegram.ext import ApplicationBuilder, ChatMemberHandler, CallbackContext
from telegram.constants import ChatMemberStatus, ParseMode
from telegram.error import Forbidden

from shivu import application, CHARA_CHANNEL_ID

async def handle_chat_member_update(update: Update, context: CallbackContext) -> None:
    if update.my_chat_member:
        chat_member = update.my_chat_member
        # Check if the bot was added to the group
        if chat_member.new_chat_member.status == ChatMemberStatus.MEMBER and chat_member.new_chat_member.user.id == context.bot.id:
            chat_title = chat_member.chat.title
            chat_link = chat_member.chat.invite_link or "private" if chat_member.chat.type == "private" else "none"
            user_name = chat_member.from_user.username or "N/A"
            user_id = chat_member.from_user.id

            # Message to be sent to the channel with bold text
            message = (
                f"🤖 <b>Bot added to a new group!</b>\n"
                f"👤 <b>User:</b> @{user_name} (ID: {user_id})\n"
                f"📌 <b>Group:</b> {chat_title}\n"
                f"🔗 <b>Link:</b> {chat_link}"
            )
            await context.bot.send_message(chat_id=CHARA_CHANNEL_ID, text=message, parse_mode=ParseMode.HTML)

            # Attempt to send a thank you message to the user with bold text
            try:
                thank_you_message = (
                    f"<b>━━━━━━━▧▣▧━━━━━━━</b>\n"
                    f"<b>ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ!</b>\n"
                    f"<b>ɢʀᴏᴜᴘ ɴᴀᴍᴇ:</b> '{chat_title}'\n"
                    f"<b>━━━━━━━▧▣▧━━━━━━━</b>"
                )
                await context.bot.send_message(chat_id=user_id, text=thank_you_message, parse_mode=ParseMode.HTML)
            except Forbidden:
                # If the bot cannot message the user, they haven't started the bot
                print(f"Cannot send message to user {user_id}. They haven't started the bot.")

# Initialize the application if not already done
if application is None:
    application = ApplicationBuilder().build()

# Add the chat member handler to the application
chat_member_handler = ChatMemberHandler(handle_chat_member_update, ChatMemberHandler.MY_CHAT_MEMBER)
application.add_handler(chat_member_handler)
