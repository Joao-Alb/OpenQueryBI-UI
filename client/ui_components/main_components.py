import streamlit as st
import json

# Function to display tool execution details
def display_tool_executions():
    if st.session_state.tool_executions:
        with st.expander("Tool Execution History", expanded=False):
            for i, exec_record in enumerate(st.session_state.tool_executions):
                st.markdown(f"### Execution #{i+1}: `{exec_record['tool_name']}`")
                st.markdown(f"**Input:** ```json{json.dumps(exec_record['input'])}```")
                st.markdown(f"**Output:** ```{exec_record['output'][:250]}...```")
                st.markdown(f"**Time:** {exec_record['timestamp']}")
                st.divider()

def format_ai_output(content:list)->str:
    formated = ""
    for message in content:
        if message["type"] == "text":
            formated += message['text']+"\n\n\n\n"
        elif message["type"] == "tool_use":
            formated += f"Using tool {message['name']} with the following inputs: {message['input']}\n"
    return formated or "didmnt work"


import pandas as pd 
import sqlite3
from time import time
def get_dataframe_from_sql(database_path:str,query:str,limit:int=100):
    """Get a dataframe from a SQL query. This will return a dataframe with the result of the query.
    """
    if "limit" not in query.lower():
        query = f"{query} LIMIT {limit}"
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    conn.close()
    return pd.DataFrame(result, columns=columns)

def plot_line_from_sql(database_path:str,query:str,x:str,y:str,limit:int=100):
    """Plot a line chart from a SQL query. This will create a line chart with the x and y values.
    """
    df = get_dataframe_from_sql(database_path,query,limit)
    if x not in df.columns or y not in df.columns:
        raise ValueError(f"Columns {x} and {y} must be present in the dataframe.")
    return st.line_chart(df.set_index(x)[y])

def plot_bar_from_sql(database_path:str,query:str,x:str,y:str,limit:int=100):
    """Plot a bar chart from a SQL query using Streamlit. This will create a bar chart with the x and y values.
    """
    df = get_dataframe_from_sql(database_path,query,limit)
    st.write(df)
    if x not in df.columns or y not in df.columns:
        raise ValueError(f"Columns {x} and {y} must be present in the dataframe.")
    return st.bar_chart(df.set_index(x)[y])

functions ={
    "line":plot_line_from_sql,
    "bar":plot_bar_from_sql
}

def plot_from_sql(configs:dict):
    """Plot a bar chart from a SQL query using Streamlit. This will create a bar chart with the x and y values.
    """
    df = get_dataframe_from_sql(database_path,query,limit)
    if configs['x'] not in df.columns or configs['y'] not in df.columns:
        raise ValueError(f"Columns {configs['x']} and {configs['y']} must be present in the dataframe.")
    
    while True:
        st.empty()  # clear old content
        return functions[configs['type']](df.set_index(configs['x'])[configs['y']])
        time.sleep(configs['update_interval'])
        st.rerun()