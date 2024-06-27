import streamlit as st
from pipeline import summary_pipeline

st.set_page_config(page_title="Website Summarizer", page_icon="📝")
st.title("Website Summarizer")

# My Side-bar:
with st.sidebar:
    side_bar_title = "## Configure API key"
    st.markdown(side_bar_title)
    with st.form(key="api-key-form", clear_on_submit=True, border=False):
        api_key = st.text_input(
            label="Enter your Nvidia NIM API key:",
            type='password',
        )
        _, c1 = st.columns([2.25, 0.75])
        if c1.form_submit_button(label="Send", type='secondary'):
            st.info(body="Your API KEY has succesufely stored", icon="✅️")    
        

# My main content
with st.container():
    url = st.chat_input(placeholder="Enterer Website's URL")
    if url:
        with st.chat_message(name='ai'):
            with st.spinner("generating your summary..."):
                summary = summary_pipeline(url=url, api_key=api_key)
            st.info(summary)