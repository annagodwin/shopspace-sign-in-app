
import streamlit as st
from utils.utilities import get_button_color_markdown_formatting, switch_page, get_shopspace_logo
import time

# ===========
#    SETUP 
# ===========

# sidebar config
st.set_page_config(initial_sidebar_state="collapsed")

# button config
m = get_button_color_markdown_formatting()

# load assets
logo_image = get_shopspace_logo()


# ===========
#     APP 
# ===========
# Logo / Title
st.image(image=logo_image, use_column_width=True)
st.text(" ")
st.markdown("<h3 style='text-align: center; color: black;'>Thank you for signing in!</h3>", unsafe_allow_html=True)
st.text(" ")
st.text(" ")

# Buttons
col1, col2, col3 = st.columns([1,1,1])
home_button = col2.button("Back to Sign-In Page", use_container_width=True)

if home_button:
    switch_page("sign_in_home")

time.sleep(3)
switch_page("sign_in_home")
