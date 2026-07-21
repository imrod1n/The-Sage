import discord
import os
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

def ask_ai(prompt):
    response = client_ai.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

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

        answer = ask_ai(user_text)

        await message.channel.send(answer)

client.run(TOKEN)