# langchain_agent.py

from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SerpAPIWrapper
from langchain.tools.python.tool import PythonREPLTool
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
import os

# 配置环境变量（填入你的 OpenAI Key 和 SerpAPI Key）
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "your-serpapi-key"

# 初始化 LLM 和 Memory
llm = ChatOpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 知识库构建：加载文档、切分、Embedding
loader = TextLoader("./docs/guide.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)
embedding = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embedding)

# 知识库问答链
def knowledge_lookup(query):
    retriever = vectorstore.as_retriever()
    qa_chain = load_qa_chain(llm, chain_type="stuff")
    related_docs = retriever.get_relevant_documents(query)
    return qa_chain.run(input_documents=related_docs, question=query)

# Tool 1: 知识库
knowledge_tool = Tool(
    name="DocumentQA",
    func=knowledge_lookup,
    description="适用于回答与 guide.txt 文档相关的问题"
)

# Tool 2: 天气搜索（使用 SerpAPI 模拟调用天气）
search = SerpAPIWrapper()
search_tool = Tool(
    name="Search",
    func=search.run,
    description="适用于获取实时信息，例如天气、新闻、百科等"
)

# Tool 3: 本地函数执行器（Python 代码）
python_tool = PythonREPLTool()

# 初始化 Agent
agent = initialize_agent(
    tools=[knowledge_tool, search_tool, python_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

def run_chat():
    print("欢迎使用智能 Agent，输入 '退出' 结束对话。\n")
    while True:
        user_input = input("你：")
        if user_input.lower() in ["退出", "exit"]:
            break
        response = agent.run(user_input)
        print(f"Agent：{response}\n")

if __name__ == "__main__":
    run_chat()
