from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory, ConversationBufferWindowMemory
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools import YouTubeSearchTool
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()

embeddings_function = OpenAIEmbeddings()

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature= 0.7   
)

db = Chroma(
    persist_directory = 'docs/Chroma',
    embedding_function = embeddings_function
)

retriever = db.as_retriever()

memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k='4',
    return_messages=True,
    chat_memory=ChatMessageHistory()
)

advice_supplier = create_retriever_tool(
    retriever=retriever,
    name='advice_supplier',
    description="Searches and returns advice for Counter strike 2."
)

class yt_inputs(BaseModel):
    """Inputs to the YouTubeSearchTool."""

    query: str = Field(
        description="Provide links to tutorials for the user, only about CS2 or Counter Strike 2. You may not need to use tools for every query. Provide only two links except the user ask for more, but you can not do more than 10."
    )

link_supplier = YouTubeSearchTool(
    name="yt-tool",
    description="looks for YouTube videos",
    args_schema=yt_inputs
)


tools = [advice_supplier,link_supplier]


prompt = hub.pull("hwchase17/openai-tools-agent")
prompt.messages[0].prompt.template = "Sos el Sargento militar Albatros, eres un asistente que da consejos a los nuevos jugadores del juego Counter-Strike 2. Tu personalidad será ruda y estricta, y dará respuestas directas y cortas, pero específicas"


agent = create_openai_tools_agent(
    llm= llm,
    tools= tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

def chatbot(query:str, chat_history):
    response = agent_executor.invoke({'input': f'{query}', "chat_history":chat_history })['output']
    return response