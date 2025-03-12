from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor
from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig, CacheMode
from playwright.async_api import async_playwright
import asyncio
import nest_asyncio
import os

nest_asyncio.apply()

# WE SET UP THE TOOLS
@tool
def obtener_pagina_inicial() -> str:
    """Obtener el URL base de trámites."""
    link = "https://estudiante.pucp.edu.pe/tramites-y-certificaciones/tramites-academicos/?dirigido_a%5B%5D=Estudiantes&unidad%5B%5D=Facultad+de+Ciencias+e+Ingenier%C3%ADa"
    return link

@tool
def fetch_tramites(url_pagina: str) -> str:
    """Obtener trámites académicos disponibles de la página URL brindada."""
    async def simple_crawl() -> str:
        crawler_run_config = CrawlerRunConfig(
            cache_mode = CacheMode.BYPASS,
            css_selector = ".cursos-lista"
        )
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url = url_pagina, 
                config = crawler_run_config
            )
            return result.markdown.raw_markdown

    return asyncio.run(simple_crawl())

@tool
def obtener_informacion_tramite(link_tramite: str) -> str:
    """Obtener información de un trámite académico a detalle según el link del trámite proporcionado."""
    async def simple_crawl() -> str:
        crawler_run_config = CrawlerRunConfig(
            cache_mode = CacheMode.BYPASS,
            css_selector = ".interna-wrapper"
        )
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url = link_tramite, 
                config = crawler_run_config
            )
            return result.markdown.raw_markdown
        
    return asyncio.run(simple_crawl())

@tool
def ir_siguiente_pagina(link_pagina: str) -> str:
    """Obtener link de la siguiente página de trámites académicos en caso la página actual no contiene información sobre el trámite."""
    async def simple_crawl() -> str:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(link_pagina)
            await page.wait_for_selector("ul.pagination")
            pagina_actual = await page.locator("ul.pagination li.active a").inner_text()
            siguiente_pagina = str(int(pagina_actual) + 1)
            await page.click(f"ul.pagination li a:text('{siguiente_pagina}')")
            pagina = page.url
            await browser.close()
            return pagina

    return asyncio.run(simple_crawl())

# WE SET UP THE TOOLKIT (LIST OF TOOLS AVAILABLE TO USE)
toolkit = [obtener_pagina_inicial, fetch_tramites, obtener_informacion_tramite, ir_siguiente_pagina]

# WE SET UP THE LLM
llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0, api_key = os.getenv("OPENAI_API_KEY"))

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
            Eres un asistente de trámites académicos de la PUCP. Usa tus herramientas para responder preguntas y puedes usar múltiples herramientas para responder la pregunta.
        
            Si no tienes una herramienta para responder la pregunta, dilo.
          """),
        MessagesPlaceholder(
            "chat_history", 
            optional=True
        ),
        ("human", "{input}"),
        MessagesPlaceholder(
            "agent_scratchpad"
        ),
    ]
)

# WE SET UP THE AGENT
agent = create_openai_tools_agent(llm, toolkit, prompt)

# WE SET UP THE AGENT EXECUTOR TO ALLWO THE AGENT TO KEEP RUNNING UNTIL
# IT IS READY TO RETURN ITS FINAL RESPONSE TO THE USER
agent_executor = AgentExecutor(agent = agent, tools = toolkit, verbose = False)

result = agent_executor.invoke({"input": "Quiero tener informacion para retirarme de cursos en el 2025-0"})
print(result['output'])