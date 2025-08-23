import streamlit as st
import asyncio
import os
import sys
import nest_asyncio
import atexit

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from services.chat_service import init_session
from utils.async_helpers import on_shutdown
from apps import openquerybi_ui

# Apply nest_asyncio to allow nested asyncio event loops (needed for Streamlit's execution model)
nest_asyncio.apply()

page_icon_path = os.path.join('.', 'icons', 'OpenQueryBI_icon.png')

st.set_page_config(
                   page_title="OpenQueryBI",
                   page_icon=(page_icon_path),
                   layout='wide',
                   initial_sidebar_state="expanded"
                    )

# Customize css
with open(os.path.join('.', '.streamlit', 'style.css')) as f:
   st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def main():
    # Initialize session state for event loop
    if "loop" not in st.session_state:
        st.session_state.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(st.session_state.loop)
    
    # Register shutdown handler
    atexit.register(on_shutdown)
    
    # Initialize the primary application
    init_session()
    openquerybi_ui.main()

if __name__ == "__main__":
    main()