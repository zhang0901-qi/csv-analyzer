from langchain.agents.self_ask_with_search.prompt import PROMPT
from langchain.chains.flare.prompts import PROMPT_TEMPLATE
import json
from langchain_community.chat_models import ChatTongyi
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent#创建DataFrame agent 执行器的函数

#判断前端展示方式：表格、字符串、图表
PROMPT_TEMPLATE = """
你是一位数据分析助手，你的回答内容取决于用户的请求内容。

1.对于文字回答的问题，按照这样的格式回答：
  {"answer": "<你的答案写在这里>"}
例如：
  {"answer": "<订单量最高的产品ID是LMNWC3-067>"}
  
2.如果用户需要一个表格，按照这样的格式回答：
  {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...],]}}
  
3.如果用户的请求适合返回条形图，按照这样的格式回答：
  {"bar": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}
  
4.如果用户的请求适合返回折线图，按照这样的格式回答：
  {"line": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}
  
5.如果用户的请求适合返回散点图，按照这样的格式回答：
  {"scatter": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}
注意：我们只支持三种类型的图表: "bar", "line" 和 "scatter"。

请将所有输出作为JSON字符串返回。请注意要将"columns"列表和数据列表中的所有字符串都用双引号包围。
例如：{"columns": ["Products", "Orders"], "data": [["32085Lip", 245, ["76439Eye", 178]]}

你要处理的用户请求如下：
"""

def dataframe_agent(qwen_api_key, df, query):
    model = ChatTongyi(model="qwen_turbo",
                       api_key=qwen_api_key,
                       temperature=0)

    #开始定义agent执行器
    agent = create_pandas_dataframe_agent(llm=model,
                                  df=df,
                                  agent_executor_kwargs={"handle_parsing_errors": True},#最后一个是尽可能让模型自行消化和处理错误，而不是让模型终止
                                  verbose=True)#在终端可以看到执行过程
    #把用户的要求和补充的要求拼接起来
    prompt = PROMPT_TEMPLATE + query
    response = agent.invoke({"input": prompt})

    #把response返回的字符出输出继续解析成字典，方便前端使用。调用json的loads方法，传入要解析的字符串，就是response里面的output
    response_dict = json.loads(response["output"])
    return response_dict

#import os
#import pandas as pd#pandas是一个强大灵活的数据分析库，提供易于使用的数据结构
#df = pd.read_csv("personal_data.csv")
#print(dataframe_agent(os.getenv("DASHSCOPE_API_KEY"), df, "问题"))