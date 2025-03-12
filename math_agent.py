from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor
import os

#setting up the tools
@tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@tool
def square(a) -> int:
    """Calculates the square of a number."""
    a = int(a)
    return a * a

# print(add.name)
# print(add.description)
# print(add.args)

#setting up the toolkit which are an the list of tools
toolkit = [add, multiply, square]

#setting up the llm
llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0, api_key = os.getenv("OPENAI_API_KEY"))

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
          You are a mathematical assistant. Use your tools to answer questions and you can use multiple tools to answer the question.
          If you do not have a tool to answer the question, say so. 
        
          Return only the answers. e.g
          Human: What is 1 + 1?
          AI: 2
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

#setting up the agent
agent = create_openai_tools_agent(llm, toolkit, prompt)

#in order to run agents in langchain they need to be run via agent executor
#acts as the runtime for agents in LangChain, and allow an agent to 
#keep running until it is ready to return its final response to the user.
#we are setting verbose to True so we can get an idea of what the agent 
#is doing as it is processing our request

agent_executor = AgentExecutor(agent = agent, tools = toolkit, verbose = True)

result = agent_executor.invoke({"input": "what is 5 squared?"})
print(result['output'])