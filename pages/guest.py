import streamlit as st
from streamlit.runtime.scriptrunner import RerunData, RerunException
from streamlit.source_util import get_pages
import streamlit.components.v1 as components

from pathlib import Path
from PIL import Image
import time

# === PAGE SETTINGS === 
# disable sidebar
st.set_page_config(initial_sidebar_state="collapsed")

# SWITCH PAGE BUTTON ===
def switch_page(page_name: str):

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("src/sign_in_app/home.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")


# === PAGE SETTINGS ===
# button base color formatting & on hover formatting
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #F7D47F;
    color:black;
}
div.stButton > button:hover {
    background-color: #F7AD2F;
    color:black;
    }
</style>
""", unsafe_allow_html=True)


# === LOAD ASSETS ===
logo_image = Image.open(Path('resources/logo/ShopSpace-YellowLogo1200x320.png'))


# === APP ===

# Image
st.image(image=logo_image, use_column_width=True)

st.text(" ")
# Embed Form
components.iframe("https://docs.google.com/forms/d/e/1FAIpQLSdLXE7GoJYUKEjpuxHn_jhnJ62QJMTi-_4hvsspaKJiIZ7NWw/viewform?embedded=true",
                  width=640, height=500, scrolling=True)

st.text(" ")
# Buttons
col1, col2, col3 = st.columns([1,1,1])


# time.sleep(10)
complete_button = col2.button(label="I've completed the form and clicked the Submit button", use_container_width=True)

if complete_button:
    switch_page("thank_you")


