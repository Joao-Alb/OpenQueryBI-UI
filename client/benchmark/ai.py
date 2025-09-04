from utils.async_helpers import run_async
import streamlit as st
from services.mcp_service import run_agent
from utils.ai_prompts import make_main_prompt
from langchain_core.messages import ToolMessage, HumanMessage

def get_sql_from_ai(prompt:str)->str:
    prompt = make_main_prompt(prompt,language='spider-benchmark')
    ans = run_async(run_agent(st.session_state.agent, prompt))
    return find_sql_in_text(ans)

def find_sql_in_text(response)->str:
    for msg in response["messages"][::-1]:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tool_call in msg.tool_calls[::-1]:
                if "validate_query" in tool_call['name']:
                    return clean_sql(str(tool_call['args']['query']))

def clean_sql(sql:str)->str:
    return sql.strip().rstrip(';')

def format_message(response)->str:
    messages = []
    for msg in response["messages"]:
        if not (isinstance(msg, ToolMessage) or isinstance(msg, HumanMessage)):
            if hasattr(msg, "content") and msg.content:
                messages.append(format_output(msg.content) if type([])==type(msg.content) else str(msg.content))
    return "\n".join(messages)

def format_output(content:list)->str:
    formated = ""
    for message in content:
        if message["type"] == "text":
            formated += message['text']+"\n"
    return formated

def get_msgs_from_ai(prompt:str)->str:
    prompt = make_main_prompt(prompt,language='en')
    ans = run_async(run_agent(st.session_state.agent, prompt))
    formatted = format_message(ans)
    return formatted