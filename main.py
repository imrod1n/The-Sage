import discord
from discord import app_commands
import asyncio
import logging
import config
from ai import ask_ai, user_context


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

TOKEN = config.DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)


@tree.command(name="help", description="Показать команды")
async def cmd_help(interaction: discord.Interaction):
    await interaction.response.send_message(config.BOT_HELP_TEXT)
    return

@tree.command(name="reset", description="Сбросить контекст")
async def cmd_reset(interaction: discord.Interaction):
    user_context[interaction.user.id] = []
    await interaction.response.send_message(config.CONTEXT_RESET_MESSAGE)
    return
    
@client.event
async def on_ready():
    logging.info(f"Бот запущен как {client.user}")
    await tree.sync()
    logging.info(f"Команды синхронизированы")

@client.event
async def on_message(message):
    logging.info(f"{message.author} ({message.author.id}): {message.content}")
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
        logging.info(f"Ответ бота: {answer}")

client.run(TOKEN)