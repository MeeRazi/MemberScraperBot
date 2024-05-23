import os, logging, asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
GROUP_ID = os.getenv("GROUP_ID")

logging.basicConfig(level=logging.INFO)

bot = Client("MemberScraper", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

added = 0
@bot.on_message(filters.command("scrap") & filters.me)
async def scrap_members(client, message):
    chat_id = message.chat.id
    members = await client.get_chat_members(chat_id)
    for member in members:
        try:
            success = await client.add_chat_members(chat_id, member.user.id)
            if success:
                added += 1
                logging.info(f"Added {member.user.id} to chat")
        except FloodWait as e:
            logging.warning(f"FloodWait for {e.x} seconds")
            await asyncio.sleep(e.x)
        except Exception as e:
            logging.error(f"Failed to add {member.user.id} to chat: {e}")
    await client.send_message("me", text=f"Added {added}/{len(members)} members to chat")