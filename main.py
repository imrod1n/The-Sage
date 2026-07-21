import discord
import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

client_ai = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

user_context = {}

def ask_ai(user_id, prompt):
    if user_id not in user_context:
        user_context[user_id] = []

    user_context[user_id].append({"role": "user", "content": prompt})
    user_context[user_id] = user_context[user_id][-6:]

    response = client_ai.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=user_context[user_id],
        max_tokens=300
    )
    answer = response.choices[0].message.content
    user_context[user_id].append({"role": "assistant", "content": answer})
    return answer

@client.event
async def on_ready():
    print(f'Бот запущен как {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = message.content.lower()

    if text.startswith("мудрец"):
        user_text = message.content[7:]

        if not user_text:
            await message.channel.send("Спроси что-нибудь 🙂")
            return

        answer = await asyncio.to_thread(ask_ai, message.author.id, user_text)
        await message.channel.send(answer)

client.run(TOKEN)