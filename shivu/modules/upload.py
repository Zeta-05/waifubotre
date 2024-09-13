#▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
# For Waifu/Husbando telegram bots.
# Updated and Added new commands, features and style by https://github.com/lovetheticx
#▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

# <======================================= IMPORTS ==================================================>
import urllib.request
from pymongo import ReturnDocument
import os
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from PIL import Image, ImageDraw, ImageFont
from shivu import application, sudo_users, collection, db, CHARA_CHANNEL_ID, SUPPORT_CHAT
from gridfs import GridFS

from io import BytesIO

WRONG_FORMAT_TEXT = """Wrong ❌️ format...  eg. /upload Img_url muzan-kibutsuji Demon-slayer 3

img_url character-name anime-name rarity-number

use rarity number accordingly rarity Map

rarity_map = 
1 (⚪️ Common) 
2 (🟣 Rare)
3 (🟢 Medium) 
4 (🟡 Legendary) 
5 (🔮 Limited) 
6 (💮 Special) 
7 (🎐 Celestial)

EVENT_MAPPING = {
    1: 𝑺𝒖𝒎𝒎𝒆𝒓 🏖},
    2: 𝑲𝒊𝒎𝒐𝒏𝒐 👘},
    3: 𝑾𝒊𝒏𝒕𝒆𝒓 ❄️},
    4: 𝑽𝒂𝒍𝒆𝒏𝒕𝒊𝒏𝒆 💞},
    5: 𝑺𝒄𝒉𝒐𝒐𝒍 🎒},
    6: 𝑯𝒂𝒍𝒍𝒐𝒘𝒆𝒆𝒏 🎃},
    7: 𝑮𝒂𝒎𝒆 🎮},
    8: 𝑴𝒂𝒓𝒊𝒏𝒆 🪼},
    9: 𝑩𝒂𝒔𝒌𝒆𝒕𝒃𝒂𝒍𝒍 🏀},
    10: 𝑴𝒂𝒊𝒅 🧹},
    11: 𝑹𝒂𝒊𝒏 ☔},
    12: 𝑩𝒖𝒏𝒏𝒚 🐰},
    13: 𝑩𝒍𝒐𝒔𝒔𝒐𝒎 🌸},
    14: 𝑹𝒐𝒄𝒌 🎸},
    15: 𝑪𝒉𝒓𝒊𝒔𝒕𝒎𝒂𝒔 🎄},
    16: 𝑵𝒆𝒓𝒅 🤓},
    17: 𝑾𝒆𝒅𝒅𝒊𝒏𝒈 💍},
    18: 𝑪𝒉𝒆𝒆𝒓𝒍𝒆𝒂𝒅𝒆𝒓𝒔 🎊},
    19: 𝑨𝒓𝒕𝒊𝒔𝒕 🎨},
    20: 𝑵𝒖𝒓𝒔𝒆 🏨},
    21: None  # Skip event"""

EVENT_MAPPING = {
    1: {"name": "𝑺𝒖𝒎𝒎𝒆𝒓", "sign": "🏖"},
    2: {"name": "𝑲𝒊𝒎𝒐𝒏𝒐", "sign": "👘"},
    3: {"name": "𝑾𝒊𝒏𝒕𝒆𝒓", "sign": "❄️"},
    4: {"name": "𝑽𝒂𝒍𝒆𝒏𝒕𝒊𝒏𝒆", "sign": "💞"},
    5: {"name": "𝑺𝒄𝒉𝒐𝒐𝒍", "sign": "🎒"},
    6: {"name": "𝑯𝒂𝒍𝒍𝒐𝒘𝒆𝒆𝒏", "sign": "🎃"},
    7: {"name": "𝑮𝒂𝒎𝒆", "sign": "🎮"},
    8: {"name": "𝑴𝒂𝒓𝒊𝒏𝒆", "sign": "🪼"},
    9: {"name": "𝑩𝒂𝒔𝒌𝒆𝒕𝒃𝒂𝒍𝒍", "sign": "🏀"},
    10: {"name": "𝑴𝒂𝒊𝒅", "sign": "🧹"},
    11: {"name": "𝑹𝒂𝒊𝒏", "sign": "☔"},
    12: {"name": "𝑩𝒖𝒏𝒏𝒚", "sign": "🐰"},
    13: {"name": "𝑩𝒍𝒐𝒔𝒔𝒐𝒎", "sign": "🌸"},
    14: {"name": "𝑹𝒐𝒄𝒌", "sign": "🎸"},
    15: {"name": "𝑪𝒉𝒓𝒊𝒔𝒕𝒎𝒂𝒔", "sign": "🎄"},
    16: {"name": "𝑵𝒆𝒓𝒅", "sign": "🤓"},
    17: {"name": "𝑾𝒆𝒅𝒅𝒊𝒏𝒈", "sign": "💍"},
    18: {"name": "𝑪𝒉𝒆𝒆𝒓𝒍𝒆𝒂𝒅𝒆𝒓𝒔", "sign": "🎊"},
    19: {"name": "𝑨𝒓𝒕𝒊𝒔𝒕", "sign": "🎨"},
    20: {"name": "𝑵𝒖𝒓𝒔𝒆", "sign": "🏨"},
    21: None  # Skip event
}


async def get_next_sequence_number(sequence_name):
    sequence_collection = db.sequences
    sequence_document = await sequence_collection.find_one_and_update(
        {'_id': sequence_name}, 
        {'$inc': {'sequence_value': 1}}, 
        return_document=ReturnDocument.AFTER
    )
    if not sequence_document:
        await sequence_collection.insert_one({'_id': sequence_name, 'sequence_value': 0})
        return "0000"
    
    sequence_number = sequence_document['sequence_value']
    return str(sequence_number).zfill(4)


async def upload(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('Ask My Owner...')
        return

    try:
        args = context.args
        if len(args) != 5:
            await update.message.reply_text(WRONG_FORMAT_TEXT)
            return

        character_name = args[1].replace('-', ' ').title()
        anime = args[2].replace('-', ' ').title()

        try:
            urllib.request.urlopen(args[0])
        except:
            await update.message.reply_text('Invalid URL.')
            return

        rarity_map = {1: "⚪ Common", 2: "🟣 Rare", 3: "🟢 Medium", 4: "🟡 Legendary", 5: "🔮 Limited", 6: "💮 Special", 7: "🎐 Celestial"}
        try:
            rarity = rarity_map[int(args[3])]
        except KeyError:
            await update.message.reply_text('Invalid rarity. Please use 1, 2, 3, 4, 5, 6 or 7.')
            return
        
        event_choice = int(args[4])
        event = EVENT_MAPPING.get(event_choice)

        id = str(await get_next_sequence_number('character_id')).zfill(2)

        character = {
            'img_url': args[0],
            'name': character_name,
            'anime': anime,
            'rarity': rarity,
            'id': id,
            'event': event  # Add the event to the character data
        }

        try:
            message = await context.bot.send_photo(
                chat_id=CHARA_CHANNEL_ID,
                photo=args[0],
                caption=f'<b>ID: {id}:</b> {character_name}\n<b>ANIME: {anime}</b>\n(<b>{rarity[0]} 𝙍𝘼𝙍𝙄𝙏𝙔: </b>{rarity[2:]})' +
                        (f'\n<b>Event:</b> {event["name"]} {event["sign"]}' if event else '') + 
                        f'\n\n𝑨𝒅𝒅𝒆𝒅 𝑩𝒚 ➥ <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )
            character['message_id'] = message.message_id
            await collection.insert_one(character)
            await update.message.reply_text('CHARACTER ADDED....')
        except:
            await collection.insert_one(character)
            update.effective_message.reply_text("Character Added but no Database Channel Found, Consider adding one.")
        
    except Exception as e:
        await update.message.reply_text(f'Character Upload Unsuccessful. Error: {str(e)}\nIf you think this is a source error, forward to: {SUPPORT_CHAT}')

async def delete(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('Ask my Owner to use this Command...')
        return

    try:
        args = context.args
        if len(args) != 1:
            await update.message.reply_text('Incorrect format... Please use: /delete ID')
            return

        
        character = await collection.find_one_and_delete({'id': args[0]})

        if character:
            
            await context.bot.delete_message(chat_id=CHARA_CHANNEL_ID, message_id=character['message_id'])
            await update.message.reply_text('DONE')
        else:
            await update.message.reply_text('Deleted Successfully from db, but character not found In Channel')
    except Exception as e:
        await update.message.reply_text(f'{str(e)}')

async def update(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('You do not have permission to use this command.')
        return

    try:
        args = context.args
        if len(args) != 3:
            await update.message.reply_text('Incorrect format. Please use: /update id field new_value')
            return

        # Get character by ID
        character = await collection.find_one({'id': args[0]})
        if not character:
            await update.message.reply_text('Character not found.')
            return

        # Check if field is valid
        valid_fields = ['img_url', 'name', 'anime', 'rarity', 'event']
        if args[1] not in valid_fields:
            await update.message.reply_text(f'Invalid field. Please use one of the following: {", ".join(valid_fields)}')
            return

        # Update field
        if args[1] in ['name', 'anime']:
            new_value = args[2].replace('-', ' ').title()
        elif args[1] == 'rarity':
            rarity_map = {1: "⚪ Common", 2: "🟣 Rare", 3: "🟢 Medium", 4: "🟡 Legendary", 5: "🔮 Limited", 6: "💮 Special", 7:"🎐 Celestial"}
            try:
                new_value = rarity_map[int(args[2])]
            except KeyError:
                await update.message.reply_text('Invalid rarity. Please use 1, 2, 3, 4, 5, 6 or 7.')
                return
        elif args[1] == 'event':
            event_map = {
                1: {"name": "𝑺𝒖𝒎𝒎𝒆𝒓", "sign": "🏖"},
                2: {"name": "𝑲𝒊𝒎𝒐𝒏𝒐", "sign": "👘"},
                3: {"name": "𝑾𝒊𝒏𝒕𝒆𝒓", "sign": "❄️"},
                4: {"name": "𝑽𝒂𝒍𝒆𝒏𝒕𝒊𝒏𝒆", "sign": "💞"},
                5: {"name": "𝑺𝒄𝒉𝒐𝒐𝒍", "sign": "🎒"},
                6: {"name": "𝑯𝒂𝒍𝒍𝒐𝒘𝒆𝒆𝒏", "sign": "🎃"},
                7: {"name": "𝑮𝒂𝒎𝒆", "sign": "🎮"},
                8: {"name": "𝑴𝒂𝒓𝒊𝒏𝒆", "sign": "🪼"},
                9: {"name": "𝑩𝒂𝒔𝒌𝒆𝒕𝒃𝒂𝒍𝒍", "sign": "🏀"},
                10: {"name": "𝑴𝒂𝒊𝒅", "sign": "🧹"},
                11: {"name": "𝑹𝒂𝒊𝒏", "sign": "☔"},
                12: {"name": "𝑩𝒖𝒏𝒏𝒚", "sign": "🐰"},
                13: {"name": "𝑩𝒍𝒐𝒔𝒔𝒐𝒎", "sign": "🌸"},
                14: {"name": "𝑹𝒐𝒄𝒌", "sign": "🎸"},
                15: {"name": "𝑪𝒉𝒓𝒊𝒔𝒕𝒎𝒂𝒔", "sign": "🎄"},
                16: {"name": "𝑵𝒆𝒓𝒅", "sign": "🤓"},
                17: {"name": "𝑾𝒆𝒅𝒅𝒊𝒏𝒈", "sign": "💍"},
                18: {"name": "𝑪𝒉𝒆𝒆𝒓𝒍𝒆𝒂𝒅𝒆𝒓𝒔", "sign": "🎊"},
                19: {"name": "𝑨𝒓𝒕𝒊𝒔𝒕", "sign": "🎨"},
                20: {"name": "𝑵𝒖𝒓𝒔𝒆", "sign": "🏨"},
                21: None  # Skip event
            }
            try:
                new_value = event_map[int(args[2])]
            except KeyError:
                await update.message.reply_text('Invalid event. Please use a number between 1 and 13.')
                return
        else:
            new_value = args[2]

        await collection.find_one_and_update({'id': args[0]}, {'$set': {args[1]: new_value}})

        
        if args[1] == 'img_url':
            await context.bot.delete_message(chat_id=CHARA_CHANNEL_ID, message_id=character['message_id'])
            message = await context.bot.send_photo(
                chat_id=CHARA_CHANNEL_ID,
                photo=new_value,
                caption=f'<b>ID: {character["id"]}:</b> {character["name"]}\n<b>ANIME: {character["anime"]}</b>\n(<b>{character["rarity"][0]} 𝙍𝘼𝙍𝙄𝙏𝙔:</b> {character["rarity"][2:]})\n{character["event"]["sign"] if character.get("event") else ""}\n\n𝑼𝒑𝒅𝒂𝒕𝒆𝒅 𝑩𝒚 ➥ <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )
            character['message_id'] = message.message_id
            await collection.find_one_and_update({'id': args[0]}, {'$set': {'message_id': message.message_id}})
        else:
            caption = f'<b>{character["id"]}:</b> {character["name"]}\n<b>{character["anime"]}</b>\n(<b>{character["rarity"][0]} 𝙍𝘼𝙍𝙄𝙏𝙔:</b> {character["rarity"][2:]})\n'
            if character.get("event"):
                caption += f'{character["event"]["sign"]} {character["event"]["name"]}\n'
            caption += f'\n𝑼𝒑𝒅𝒂𝒕𝒆𝒅 𝑩𝒚 ➥ <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>'

            await context.bot.edit_message_caption(
                chat_id=CHARA_CHANNEL_ID,
                message_id=character['message_id'],
                caption=caption,
                parse_mode='HTML'
            )

        await update.message.reply_text('Updated Done in Database.... But sometimes it Takes Time to edit Caption in Your Channel..So wait..')
    except Exception as e:
        await update.message.reply_text(f'I guess did not added bot in channel.. or character uploaded Long time ago.. Or character not exits.. orr Wrong id')

async def check(update: Update, context: CallbackContext) -> None:    
     try:
        args = context.args
        if len(context.args) != 1:
            await update.message.reply_text('Incorrect format. Please use: /check id')
            return
            
        character_id = context.args[0]
         # Get character name from the command arguments
        
        character = await collection.find_one({'id': args[0]}) 
            
        if character:
            # If character found, send the information along with the image URL
            message = f"<b>Character Name:</b> {character['name']}\n" \
                      f"<b>Anime Name:</b> {character['anime']}\n" \
                      f"<b>Rarity:</b> {character['rarity']}\n" \
                      f"<b>ID:</b> {character['id']}\n" \
                      f"<b>Event:</b> {character['event'].get('name') if character.get('event') else 'None'}\n" 

            await context.bot.send_photo(chat_id=update.effective_chat.id,
                                         photo=character['img_url'],
                                         caption=message,
                                         parse_mode='HTML')
        else:
            await update.message.reply_text("Character not found.")
     except Exception as e:
        await update.message.reply_text(f"Error occurred: {e}")


async def check_total_characters(update: Update, context: CallbackContext) -> None:
    try:
        total_characters = await collection.count_documents({})
        
        await update.message.reply_text(f"Total number of characters: {total_characters}")
    except Exception as e:
        await update.message.reply_text(f"Error occurred: {e}")


async def add_sudo_user(update: Update, context: CallbackContext) -> None:
    if int(update.effective_user.id) == 6558846590:  # Replace OWNER_ID with the ID of the bot owner
        if update.message.reply_to_message and update.message.reply_to_message.from_user:
            new_sudo_user_id = str(update.message.reply_to_message.from_user.id)
            if new_sudo_user_id not in sudo_users:
                sudo_users.append(new_sudo_user_id)
                await update.message.reply_text("User added to sudo users.")
            else:
                await update.message.reply_text("User is already in sudo users.")
        else:
            await update.message.reply_text("Please reply to a message from the user you want to add to sudo users.")
    else:
        await update.message.reply_text("You are not authorized to use this command.")

ADD_SUDO_USER_HANDLER = CommandHandler('add_sudo_user', add_sudo_user, block=False)
application.add_handler(ADD_SUDO_USER_HANDLER)
       
        

ADD_SUDO_USER_HANDLER = CommandHandler('addsudo', add_sudo_user, block=False)
application.add_handler(ADD_SUDO_USER_HANDLER)

        
application.add_handler(CommandHandler("total", check_total_characters))

UPLOAD_HANDLER = CommandHandler('upload', upload, block=False)
application.add_handler(UPLOAD_HANDLER)
DELETE_HANDLER = CommandHandler('delete', delete, block=False)
application.add_handler(DELETE_HANDLER)
UPDATE_HANDLER = CommandHandler('update', update, block=False)
application.add_handler(UPDATE_HANDLER)

UPLOAD_HANDLER = CommandHandler('uploads', upload, block=upload)
application.add_handler(UPLOAD_HANDLER)
DELETE_HANDLER = CommandHandler('deletes', delete, block=False)
application.add_handler(DELETE_HANDLER)
UPDATE_HANDLER = CommandHandler('updates', update, block=False)
application.add_handler(UPDATE_HANDLER)
CHECK_HANDLER = CommandHandler('check', check, block=False)
application.add_handler(CHECK_HANDLER)
# by https://github.com/lovetheticx
