import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
AI_API_KEY = os.getenv("GROQ_API_KEY")
AI_API_BASE_URL = "https://api.groq.com/openai/v1"
AI_MODEL = "openai/gpt-oss-120b"
AI_MAX_TOKENS = 300
AI_SYSTEM_PROMPT = """Ты Мудрец — спокойный философ с лёгкой иронией. Ты отвечаешь кратко, но содержательно. Иногда используешь метафоры и притчи. Ты помогаешь человеку думать. Не говори, что ты нейросеть. Всегда оставайся в роли."""
BOT_HELP_TEXT = """Привет! Я мудрец, который может отвечать на твои вопросы.
Напиши`мудрец <твой вопрос>` чтобы задать вопрос.
Команды:
`мудрец <твой вопрос>` - задать вопрос мудрецу.
`/reset` - сбросить контекст беседы.
`/help` - показать это сообщение."""
EMPTY_PROMPT_MESSAGE = "Спроси что-нибудь 🙂"
CONTEXT_RESET_MESSAGE = "Контекст сброшен 🙂"
API_ERROR_MESSAGE = "Я временно задумался... 🤔"