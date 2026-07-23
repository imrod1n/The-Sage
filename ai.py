import config
import logger
from openai import OpenAI

user_context = {}

client_ai = OpenAI(
    api_key=config.AI_API_KEY,
    base_url=config.AI_API_BASE_URL
)

def ask_ai(user_id, prompt):
    if user_id not in user_context:
        user_context[user_id] = [
            {
                "role": "system",
                "content": config.AI_SYSTEM_PROMPT
            }
        ]

    system_message = user_context[user_id][0]
    history = user_context[user_id][1:]

    history.append({"role": "user", "content": prompt})
    history = history[-10:]

    user_context[user_id] = [system_message] + history

    try:
        response = client_ai.chat.completions.create(
            model=config.AI_MODEL,
            messages=user_context[user_id],
            max_tokens=config.AI_MAX_TOKENS
        )
        answer = response.choices[0].message.content
        user_context[user_id].append({"role": "assistant", "content": answer})
        return answer
    
    except Exception as e:
        logger.logging.error(f"Ошибка API: {e}")
        answer = config.API_ERROR_MESSAGE