"""
Приклад клієнта для AUTO.RIA MCP сервера
Використання: python3.12 clients/pydantic_ai_auto_ria_search.py

Отримання API ключа:
https://developers.ria.com/account/
"""
import asyncio
import logfire
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv
import os

# Завантажуємо змінні оточення
load_dotenv()

# Шлях до AUTO.RIA MCP сервера
mcp_server_script_path = 'servers/mcp-server-auto-ria-search.py'

# Створюємо екземпляр MCPServerStdio для підключення до AUTO.RIA MCP сервера
mcp_server = MCPServerStdio(
    command="python",
    args=[mcp_server_script_path],
    tool_prefix="auto_ria"  # Префікс для інструментів AUTO.RIA
)

# Ініціалізуємо LLM (можете замінити на свою модель)
llm = OpenAIModel(
    model_name="Qwen/Qwen3-32B-AWQ",  # назва вашої моделі
    provider=OpenAIProvider(base_url='http://127.0.0.1:8000/v1'),  # URL vLLM/Ollama API
)

# Створюємо агент pydantic_ai з LLM та AUTO.RIA MCP сервером
agent = Agent(llm, mcp_servers=[mcp_server])

# Налаштування Logfire
logfire.configure(send_to_logfire=False)
logfire.instrument_pydantic_ai()

async def main():
    """Основна функція для демонстрації AUTO.RIA MCP сервера"""

    async with agent.run_mcp_servers():
        print("🚗 AUTO.RIA MCP Server Demo")
        print("=" * 50)

        # 1. Перевіряємо доступні інструменти
        print("\n1. Перевіряємо доступні інструменти:")
        result = await agent.run('Які інструменти AUTO.RIA доступні?')
        print(result.output)

        # 2. Встановлюємо API ключ (замініть на свій)
        # Отримати API ключ можна на https://api2.ria.com/
        api_key = os.getenv("AUTO_RIA_API_KEY", "your_api_key_here")
        print("api_key", api_key)

        print(f"\n2. Встановлюємо API ключ:")
        result = await agent.run(f'Встанови API ключ AUTO.RIA: {api_key}')
        print(result.output)

        # 3. Отримуємо довідку по пошуку
        print("\n3. Отримуємо довідку по пошуку:")
        result = await agent.run('Покажи довідку по пошуку AUTO.RIA')
        print(result.output)

        # 4. Простий пошук авто
        print("\n4. Простий пошук авто (перші 5 результатів):")
        result = await agent.run(
            'Знайди перші 5 оголошень легкових авто на AUTO.RIA'
        )
        print(result.output)

        # 5. Пошук BMW з конкретними параметрами
        print("\n5. знайти BMW 2005-2010")
        result = await agent.run(
            'знайти BMW 2005-2010, покажи перші 3 результати'
        )
        print(result.output)

        # 6. Пошук авто з автоматичною коробкою
        print("\n6. Пошук авто з автоматичною коробкою:")
        result = await agent.run(
            'Знайди авто з автоматичною коробкою передач, ціна до 25000 USD'
        )
        print(result.output)

        # 7. Пошук в конкретному місті (Київ)
        print("\n7. Пошук авто в Києві:")
        result = await agent.run(
            'Знайди авто в Києві з пробігом до 100 тис. км'
        )
        print(result.output)

        # 8. Отримання детальної інформації про конкретне авто
        print("\n8. Отримуай детальну інформацію про авто 38350052")
        result = await agent.run(
            'Отримуай детальну інформацію про авто 38350052'
        )
        print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
