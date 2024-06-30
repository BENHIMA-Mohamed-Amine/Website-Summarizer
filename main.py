import streamlit as st
from pipeline import summary_pipeline

st.session_state.api_key = None
def check_api(api: str):
    if api == "":
        st.session_state.api_key = None
    else:
        if api.startswith("nvapi-"):
            st.session_state.api_key = api
        else:
            st.session_state.api_key = None



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
        c0,  c1 = st.columns([2.25, 0.75])
        c0.link_button(
            label="Get you API KEY here",
            url="https://build.nvidia.com/explore/discover"
        )
        if c1.form_submit_button(label="Send", type='secondary'):
            llm = check_api(api_key)
            if st.session_state.api_key != None:
                st.info(body="Your API KEY has succesufely stored", icon="✅️")   
        if st.session_state.api_key == None:
            st.error(
                    body="Please enter a valid API KEY",
                    icon="❗"
                ) 

# My main content
with st.container():
    url = st.chat_input(placeholder="Enter Website's URL")
    if url:
        with st.chat_message(name='ai'):
            with st.spinner("generating your summary..."):
                if st.session_state.api_key != None:   
                    try:
                        summary = summary_pipeline(url=url, api_key=st.session_state.api_key)
                        st.info(summary)
                    except Exception as e:
                        if "Unauthorized" in str(e):
                            st.error(
                                body="Please enter a valid API KEY",
                                icon="❗"
                            )
                            st.session_state.api_key = None
                        elif "Invalid URL" in str(e):
                            st.error(
                                body="Please enter a valid URL",
                                icon="❗"
                            )
                else:
                    st.error(
                        body="Please enter an API KEY first",
                        icon="❗"
                    )