from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from common.config import Config

conf = Config()

my_llm = ChatOpenAI(
    api_key = conf.MODEL_API_KEY,
    base_url = conf.MODEL_BASE_URL,
    model = conf.MODEL_NAME
)

if __name__ == '__main__':
    messages = [
        HumanMessage(content="用一句话介绍一下你自己")
    ]

    response = my_llm.invoke(messages)
    print(response.content)