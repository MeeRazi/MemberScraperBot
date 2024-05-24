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
    chat_id = message.chat.id
    m = await message.edit("Scrapping members...")
    args = message.text.split(" ")
    if len(args) < 2:
        await message.edit("Please provide source chat id")
        return
    source_chat = args[1]
    added = 0
    total = 0
    async for member in client.get_chat_members(chat_id):
        total += 1
        try:
            success = await client.add_chat_members(source_chat, member.user.id)
            if success:
                added += 1
                logging.info(f"Added {member.user.id} to chat")
                await m.edit(f"Added {added} members to chat")
                await asyncio.sleep(1)
        except FloodWait as e:
            logging.warning(f"FloodWait for {e.value} seconds")
            await asyncio.sleep(e.value)
        except Exception as e:
            logging.error(f"Failed to add {member.user.id} to chat: {e}")
    await client.send_message("me", text=f"Added {added}/{total} members to chat")

bot.run()    