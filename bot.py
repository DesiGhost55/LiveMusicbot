import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioVideoPiped
from yt_dlp import YoutubeDL

API_ID = 35887885
API_HASH = "45f9eb1dfea3aca9c9f268135fae3189"
BOT_TOKEN = "8514847398:AAFaMViA7DMVQWLpv3IKTnVe_Ekp6y4O3yE"
STRING_SESSION = "BAIjmw0ArVAHpajXOxuVtOWld3JBuD_FqNeJdPfxSFPmE6otcNNLBSupPEZxtYv7DJzB9thPp8SinCHkhn_d5RTybZUJogrc-CBkhQ67JHkYTYMq4szGaoDxWhbizVVv9PTD4bzl-fgj21j7dhLKzzgaAuj2cK3jP3y60d9podLjWyNe2Ic6-pK4qimXZOGKpxDuaZwo3F0KV3lZrZKwt1ksfJON6ICEhn24gEn48IDcLLj6ECTb59rl8cglQo3yt7tCmvgdEzUrMZxij44ABWoE_00Iuz8mTfvFyj_WGUUvG4Nd0q_0U1b651IEWqaZ-7iw8TNAbpwVQiSFe1ltGltK6R_suwAAAAH7hkKmAQ"

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_app = Client("user_bot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
call_app = PyTgCalls(user_app)

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text("👋 **हेलो भाई!**\n\nमैं लाइव वॉयस चैट म्यूजिक बोट हूँ। ग्रुप में गाना चलाने के लिए  लिखें।")

@app.on_message(filters.command("play") & filters.group)
async def play_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ गाने का नाम भी लिखो भाई!")
    
    chat_id = message.chat.id
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("🔎 गाना ढूंढ रहा हूँ...")
    
    ydl_opts = {'format': 'bestaudio/best', 'noplaylist': True, 'quiet': True}
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            audio_url = info['url']
            title = info['title']
        
        await m.edit("⚡ लाइव वॉयस चैट में जुड़ रहा हूँ...")
        await call_app.join_group_call(chat_id, AudioVideoPiped(audio_url))
        await m.edit(f"🎵 **लाइव स्ट्रीमिंग चालू भाई!**\n\n▶️ **गाना:** {title}")
        
    except Exception as e:
        await m.edit(f"❌ **एरर:** {e}")

async def main():
    await app.start()
    await user_app.start()
    await call_app.start()
    print("🚀 लाइव म्यूजिक बोट सफलतापूर्वक चालू हो गया है!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
