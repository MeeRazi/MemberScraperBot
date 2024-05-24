import os, logging, asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

logging.basicConfig(level=logging.INFO)

bot = Client("MemberScraper", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

@bot.on_message(filters.command("scrap") & filters.me)
async def scrap_members(client, message):
    args = message.text.split(" ")
    if len(args) < 3:
        await message.edit("Please provide both target and source chat ids")
        return
    target_chat, source_chat = args[1], args[2]
    is_valid_target_chat = await client.get_chat(target_chat)
    is_valid_source_chat = await client.get_chat(source_chat)
    if not is_valid_target_chat or not is_valid_source_chat:
        await message.edit("Invalid chat id")
        return
    added = 0
    total = 0
    async for member in client.get_chat_members(source_chat):
        total += 1
        try:
            success = await client.add_chat_members(target_chat, member.user.id)
            if success:
                added += 1
                logging.info(f"Added {member.user.id} to chat")
        except FloodWait as e:
            logging.warning(f"FloodWait for {e.x} seconds")
            await asyncio.sleep(e.x)
        except Exception as e:
            logging.error(f"Failed to add {member.user.id} to chat: {e}")
    await client.send_message("me", text=f"Added {added}/{total} members to chat")
    
bot.run()    