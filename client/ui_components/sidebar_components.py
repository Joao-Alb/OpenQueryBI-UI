import streamlit as st
from config import MODEL_OPTIONS, DEFAULT_TEMPERATURE, AVAILABLE_PROVIDERS
import traceback
from services.mcp_service import connect_to_mcp_servers
from services.chat_service import create_chat, delete_chat
from utils.tool_schema_parser import extract_tool_parameters
from utils.async_helpers import reset_connection_state
from utils.secrets import get_key


def create_history_chat_container():
    history_container = st.sidebar.container(height=200, border=None)
    with history_container:
        chat_history_menu = [
                f"{chat['chat_name']}_::_{chat['chat_id']}"
                for chat in st.session_state["history_chats"]
            ]
        chat_history_menu = chat_history_menu[:50][::-1]
        
        if chat_history_menu:
            current_chat = st.radio(
                label="History Chats",
                format_func=lambda x: x.split("_::_")[0] + '...' if "_::_" in x else x,
                options=chat_history_menu,
                label_visibility="collapsed",
                index=st.session_state["current_chat_index"],
                key="current_chat"
            )
            
            if current_chat:
                st.session_state['current_chat_id'] = current_chat.split("_::_")[1]

def create_benchmark_button():
    if st.session_state.benchmark["status"]:
        with st.sidebar:
            spider_benchmark_button = st.button("Start Spider Benchmark")
            if spider_benchmark_button:
                from benchmark import spider_benchmark
                spider_benchmark.main()
            text_benchmark_button = st.button("Start Text Benchmark")
            if text_benchmark_button:
                from benchmark import intratextual_benchmark
                intratextual_benchmark.main()

def create_sidebar_chat_buttons():
    with st.sidebar:
        c1, c2 = st.columns(2)
        create_chat_button = c1.button(
            "New Chat", use_container_width=True, key="create_chat_button"
        )
        if create_chat_button:
            create_chat()
            st.rerun()

        delete_chat_button = c2.button(
            "Delete Chat", use_container_width=True, key="delete_chat_button"
        )
        if delete_chat_button and st.session_state.get('current_chat_id'):
            delete_chat(st.session_state['current_chat_id'])
            st.rerun()

def create_model_select_widget():
    params = st.session_state["params"]
    params['model_id'] = st.sidebar.selectbox('🔎 Choose model',
                               options=MODEL_OPTIONS.keys(),
                               index=0)
    
def create_provider_select_widget():
    params = st.session_state.setdefault('params', {})
    # Load previously selected provider or default to the first
    default_provider = params.get("model_id", AVAILABLE_PROVIDERS[0])
    default_index = AVAILABLE_PROVIDERS.index(default_provider)
    # Provider selector with synced state
    selected_provider = st.sidebar.selectbox(
        '🔎 Choose Provider',
        options=AVAILABLE_PROVIDERS,
        index=default_index,
        key="provider_selection",
        on_change=reset_connection_state
    )
    # Save new provider and its index
    if selected_provider:
        params['model_id'] = selected_provider
        params['provider_index'] = list(MODEL_OPTIONS.keys()).index(selected_provider)
        st.sidebar.success(f"Model: {MODEL_OPTIONS[selected_provider]}")

    # Dynamic input fields based on provider
    with st.sidebar.container():
        if selected_provider == "Bedrock":
            with st.expander("🔐 Bedrock Credentials", expanded=True):
                params['region_name'] = st.text_input("AWS Region", value=params.get('region_name'),key="region_name")
                params['aws_access_key'] = st.text_input("AWS Access Key", value=params.get('aws_access_key'), type="password", key="aws_access_key")
                params['aws_secret_key'] = st.text_input("AWS Secret Key", value=params.get('aws_secret_key'), type="password", key="aws_secret_key")
        else:
            with st.expander("🔐 API Key", expanded=True):
                params['api_key'] = get_key(str(selected_provider).upper())
    

def create_advanced_configuration_widget():
    params = st.session_state["params"]
    #with st.sidebar.expander("⚙️  Basic config", expanded=False):
        #params['max_tokens'] = st.number_input("Max tokens",
                                    # min_value=1024,
                                    # max_value=10240,
                                    # value=4096,
                                    # step=512,)
        # params['temperature'] = st.slider("Temperature", 0.0, 1.0, step=0.05, value=DEFAULT_TEMPERATURE)
                
def create_mcp_connection_widget():
    with st.sidebar:
        st.subheader("Server Management")

        if st.session_state.get("agent"):
            st.success(f"📶 Connected to {len(st.session_state.servers)} MCP servers!"
                       f" Found {len(st.session_state.tools)} tools.")
        else:
            with st.spinner("Connecting to MCP servers..."):
                try:
                    connect_to_mcp_servers()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error connecting to MCP servers: {str(e)}")
                    st.code(traceback.format_exc(), language="python")