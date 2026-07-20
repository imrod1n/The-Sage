import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Бот запущен как {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    text = message.content.lower()
    if text.startswith("мудрец"):
        await message.channel.send(f"{message.author.display_name}, друг мой, я не могу ответить на это сообщение. К сожалению, я всё ещё слеп. Я скажу вам, когда прозрею.")

client.run(TOKEN)