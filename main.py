import discord
from discord import app_commands
import asyncio
import config
from ai import ask_ai, user_context
import logger
from commands import setup_commands

TOKEN = config.DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

setup_commands(tree, user_context)
    
@client.event
async def on_ready():
    logger.logging.info(f"Бот запущен как {client.user}")
    await tree.sync()
    logger.logging.info(f"Команды синхронизированы")

@client.event
async def on_message(message):
    logger.logging.info(f"{message.author} ({message.author.id}): {message.content}")
    if message.author == client.user:
        return

    text = message.content.lower()

    if text.startswith("мудрец"):
        user_text = message.content[7:]

        if not user_text:
            await message.channel.send(config.EMPTY_PROMPT_MESSAGE)
            return

        answer = await asyncio.to_thread(ask_ai, message.author.id, user_text)
        await message.channel.send(answer)
        logger.logging.info(f"Ответ бота: {answer}")

client.run(TOKEN)