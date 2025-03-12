# search-ai-agent

Panda Agent 007 is an AI Search Agent designed to crawl and extract academic procedures from the official PUCP (Pontificia Universidad Católica del Perú) student portal. It utilizes LangChain and Playwright to navigate web pages and gather information about academic procedures effectively.

## How it works

1. The agent uses the `obtener_pagina_inicial()` tool to obtain the base URL.
2. It calls `fetch_tramites()` to retrieve the list of procedures.
3. Once the agent finds the academic procedure it uses `obtener_informacion_tramite()` in order to retrieve detailed information about the aforementioned procedure.
4. If the desired information is not found on the current page, it uses `ir_siguiente_pagina()` to continue searching.

## Limitations

- Message history is currently not supported in order to maintain the agent as simple as possible.
- The tools rely slightly on CSS selectors that might change over time, although not probable.
- It requires an OpenAI API key in order to function properly.

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Install the required dependencies
   ```
   pip install -r requirements.txt
   ```
