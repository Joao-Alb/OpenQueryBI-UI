import streamlit as st
import json
from time import time

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

def display_graph_history():
    def update_data(index):
        graph = st.session_state.graphs[index]
        graph.data = get_dataframe_from_sql(graph.configs["database_configs"],graph.configs["query"],graph.configs["limit"])

    def time_to_update(graph):
        return time() - graph.last_updated >= graph.configs["update_interval"]

    while True:
        for index,graph in enumerate(st.session_state.graphs):
            if not graph.state or not time_to_update(graph):
                continue
            graph.last_updated = time()
            if graph.data is None:
                update_data(index)
                with st.expander("Graph History", expanded=False):      
                    plot_from_sql(graph.configs,graph.data)
            else:
                update_data(index)

def format_ai_output(content:list)->str:
    formated = ""
    for message in content:
        if message["type"] == "text":
            formated += message['text']+"\n\n\n\n"
        elif message["type"] == "tool_use":
            formated += f"Using tool {message['name']} with the following inputs: {message['input']}\n"
    return formated or "didmnt work"


import pandas as pd 
from sqlalchemy import create_engine,text

def __query(query: str, database_info:dict):
    if database_info['dialect'] == "sqlite":
        connection_url = f"sqlite:///{database_info['database']}"
    
    else:
       connection_url = (
        f"{database_info['dialect']}://{database_info['username']}:{database_info['password']}"
        f"@{database_info['host']}:{database_info['port']}/{database_info['database']}"
    )

    engine = create_engine(connection_url)

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall(),list(result.keys())

def get_dataframe_from_sql(database_info:dict,query:str,limit:int=100):
    """Get a dataframe from a SQL query. This will return a dataframe with the result of the query.
    """
    if "limit" not in query.lower():
        query = f"{query} LIMIT {limit}"
    result,columns = __query(query,database_info)
    return pd.DataFrame(result, columns=columns)

def plot_line_from_sql(data,x:str,y:str):
    """Plot a line chart from a SQL query. This will create a line chart with the x and y values.
    """
    if x not in data.columns or y not in data.columns:
        raise ValueError(f"Columns {x} and {y} must be present in the dataframe.")
    return st.line_chart(data.set_index(x)[y])

def plot_bar_from_sql(data,x:str,y:str):
    """Plot a bar chart from a SQL query using Streamlit. This will create a bar chart with the x and y values.
    """
    if x not in data.columns or y not in data.columns:
        raise ValueError(f"Columns {x} and {y} must be present in the dataframe.")
    return st.bar_chart(data.set_index(x)[y])

functions ={
    "line":plot_line_from_sql,
    "bar":plot_bar_from_sql
}

def plot_from_sql(configs:dict,data):
    """Plot a bar chart from a SQL query using Streamlit. This will create a bar chart with the x and y values.
    """
    if configs['x'] not in data.columns or configs['y'] not in data.columns:
        raise ValueError(f"Columns {configs['x']} and {configs['y']} must be present in the dataframe.")
    return st.markdown(f"## {configs['title']}"),functions[configs['type']](data, configs['x'], configs['y'])

class Graph():
    data:pd.DataFrame = None
    configs: dict
    state: bool = True
    last_updated: int = 0

    def __init__(self,configs, data=None):
        self.data = data or self.data
        self.configs = configs