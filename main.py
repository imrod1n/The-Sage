import discord
from discord import app_commands
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

tree = app_commands.CommandTree(client)

user_context = {}

@tree.command(name="help", description="Показать команды")
async def cmd_help(interaction: discord.Interaction):
    help_text = (
        "Привет! Я мудрец, который может отвечать на твои вопросы.\n"
        "Напиши`мудрец <твой вопрос>` чтобы задать вопрос.\n"
        "Команды:\n"
        "`мудрец <твой вопрос>` - задать вопрос мудрецу.\n"
        "`/reset` - сбросить контекст беседы.\n"
        "`/help` - показать это сообщение."
    )
    await interaction.response.send_message(help_text)
    return

@tree.command(name="reset", description="Сбросить контекст")
async def cmd_reset(interaction: discord.Interaction):
    user_context[interaction.user.id] = []
    await interaction.response.send_message("Контекст сброшен 🙂")
    return

def ask_ai(user_id, prompt):
    if user_id not in user_context:
        user_context[user_id] = []

    user_context[user_id].append({"role": "user", "content": prompt})
    user_context[user_id] = user_context[user_id][-10:]

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
    await tree.sync()
    print("Команды синхронизированы")

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