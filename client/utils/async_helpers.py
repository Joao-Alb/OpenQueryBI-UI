import streamlit as st

# Helper function for running async functions
def run_async(coro):
    """Run an async function within the stored event loop."""
    return st.session_state.loop.run_until_complete(coro)

def reset_connection_state():
    """Reset all connection-related session state variables."""
    if st.session_state.client is not None:
        try:
            # Close the existing client properly
            run_async(st.session_state.client.__aexit__(None, None, None))
        except Exception as e:
            st.error(f"Error closing previous client: {str(e)}")
    
    st.session_state.client = None
    st.session_state.agent = None
    st.session_state.tools = []

def on_shutdown():
    # Proper cleanup when the session ends
    if st.session_state.client is not None:
        try:
            # Close the client properly
            run_async(st.session_state.client.__aexit__(None, None, None))
        except Exception as e:
            st.error(f"Error during shutdown: {str(e)}")