"""
python3.12 clients/pydantic_ai_ollama_example.py
"""
import asyncio
import logfire
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

# Завантажуємо змінні оточення (наприклад, для API ключів, якщо вони потрібні LLM)
load_dotenv()

# 1. Визначаємо шлях до вашого MCP сервера
# Важливо: Шлях має бути відносним до місця запуску клієнтського скрипта
mcp_server_script_path = 'servers/mcp-server-example.py' # Переконайтеся, що шлях правильний

# 2. Створюємо екземпляр MCPServerStdio для підключення до вашого FastMCP сервера
# MCPServerStdio запустить ваш FastMCP сервер як дочірній процес і взаємодіятиме через stdio.
mcp_server = MCPServerStdio(
    command="python",
    args=[mcp_server_script_path],
    tool_prefix="my_app" # Додаємо префікс, щоб уникнути конфліктів імен інструментів
)

# 3. Ініціалізуємо LLM (вашу власну модель на vLLM або Ollama)
# Зверніть увагу: ми використовуємо ChatOpenAI з базовим URL для vLLM/Ollama
# Переконайтеся, що ваша модель vLLM/Ollama запущена і доступна за цією адресою.
# Для Ollama зазвичай: http://localhost:11434/v1
# Для vLLM зазвичай: http://localhost:8000/v1
llm = OpenAIModel(
    model_name="qwen3:0.6b", # назва вашої моделі
    provider=OpenAIProvider(base_url='http://localhost:11434/v1'), # URL вашого vLLM/Ollama API
    #
)

# 4. Створюємо агент pydantic_ai з вашою LLM та MCP сервером
agent = Agent(llm, mcp_servers=[mcp_server])

# Налаштування Logfire
logfire.configure(send_to_logfire=False)

# Інструментація pydantic_ai для генерації трасів
logfire.instrument_pydantic_ai()


async def main():
    async with agent.run_mcp_servers():
        result = await agent.run('What tools do you have?')
        print(result.output)
        result = await agent.run('Using tools `my_app_add` calc 2+3')
        print(result.output)
        result = await agent.run('Use tools `my_app_return_pi`')
        print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
