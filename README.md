# python-mcp-tutorial
Цей репозиторій демонструє, як за допомогою Python використовувати протокол MCP (Model Context Protocol)


Приклад простого MCP
```
python3.12 clients/pydantic_ai_ollama_example.py
```

Приклад клієнта для AUTO.RIA MCP сервера
```
python3.12 clients/pydantic_ai_auto_ria_search.py
```

# Запуск локальної llm vllm/olamma

## Запуск olamma
### Install
Приклад для linux. Для інших рпераційних систем дивись https://ollama.com/download
```
curl -fsSL https://ollama.com/install.sh | sh
```

### Приклад запуску моделі
```angular2html
ollama run qwen3:0.6b
```

 ### Start the server
 ```
 ollama serve
 ```

### Перевіряємо
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3:0.6b",
  "messages": [
    { "role": "user", "content": "why is the sky blue?" }
  ]
}'
```

## Приклад запуск vllm
### Start the server
```angular2html
vllm serve Qwen/Qwen3-32B-AWQ --enable-auto-tool-choice --tool-call-parser hermes  --enable-reasoning --reasoning-parser deepseek_r1
```
