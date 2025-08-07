from http.client import responses
import pandas as pd
import streamlit as st
from utils_5 import dataframe_agent


def create_chart(input_data, chart_type):
    df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
    df_data.set_index(input_data["columns"][0], inplace=True)
    if chart_type == "bar":
        st.bar_chart(df_data)
    elif chart_type == "line":
        st.line_chart(df_data)
    elif chart_type == "scatter":
        st.scatter_chart(df_data)

st.title("CSV数据分析智能工具")

with st.sidebar:
    qwen_api_key = st.text_input("请输入通义千问API密钥：", type="password")
    st.markdown("[获取通义千问API key](https://www.aliyun.com/product/pai)")

data = st.file_uploader("上传你的数据文件(CSV格式)：", type="csv")
#读取CSV文件，一边交互一边看文件
if data:
    st.session_state["df"] = pd.read_csv(data)#读取数据，并储存在对话状态里
    with st.expander("原始数据"):
        st.dataframe(st.session_state["df"])#展示数据

#给用户一个输入框
query = st.text_area("请输入你关于以上表格的问题，或数据提取请求，或可视化要求（支持散点图、条形图、折线图）：")
button = st.button("生成回答")

if button and not qwen_api_key:
    st.info("请输入通义千问API密钥")
if button and "df" not in st.session_state:
    st.info("请先上传数据文件")
if button and qwen_api_key and "df" in st.session_state:
    with st.spinner("AI正在思考中，请稍等..."):
        response_dict = dataframe_agent(qwen_api_key, st.session_state["df"], query)
        if "answer" in response_dict:
            st.write(response_dict["answer"])
        if "table" in response_dict:
            st.table(pd.DataFrame(response_dict["table"]["data"],
                                  colummns=response_dict["table"]["columns"]))
            if "bar" in response_dict:
                create_chart(response_dict["bar"], "bar")
            if "line" in response_dict:
                create_chart(response_dict["line"], "line")
            if "scatter" in response_dict:
                create_chart(response_dict["scatter"], "scatter")
