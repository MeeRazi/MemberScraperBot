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
    if len(args) != 2:
        await m.edit("Invalid command usage")
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
                await asyncio.sleep(3) # Adjust this (I dont know what is the required sleep time, so I put 3 seconds)
        except FloodWait as e:
            logging.warning(f"FloodWait for {e.value} seconds")
            await asyncio.sleep(e.value)
        except Exception as e:
            logging.error(f"Failed to add {member.user.id} to chat: {e}")
    await client.send_message("me", text=f"Added {added}/{total} members to chat")
    
@bot.on_message(filters.command(["run", "approve"], [".", "/"]))                     
async def approve(client, message):
    Id = message.chat.id
    await message.delete(True)
 
    try:
       while True:
           try:
               await client.approve_all_chat_join_requests(Id)         
           except FloodWait as t:
               asyncio.sleep(t.value)
               await client.approve_all_chat_join_requests(Id) 
           except Exception as e:
               logging.error(str(e))
    except FloodWait as s:
        asyncio.sleep(s.value)
        while True:
           try:
               await client.approve_all_chat_join_requests(Id)         
           except FloodWait as t:
               asyncio.sleep(t.value)
               await client.approve_all_chat_join_requests(Id) 
           except Exception as e:
               logging.error(str(e))

# command to delete all messages
@bot.on_message(filters.me & filters.command("clearchat", prefixes="."))
async def clearchat(_, message):
    chat_id = message.chat.id

    # send msg to show that bot is working
    await message.edit("Deleting all messages...")
    await asyncio.sleep(2)

    # get all messages
    async for msg in bot.get_chat_history(chat_id):
        try:
            # delete message
            await bot.delete_user_history(chat_id, msg.from_user.id)
        except FloodWait as e:
            # wait for a while
            print(e)
            await asyncio.sleep(e.x)
        except Exception as e:
            print(e)
            pass


bot.run()    
