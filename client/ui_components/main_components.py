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