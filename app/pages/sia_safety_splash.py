import streamlit as st
from utils.utilities import get_button_color_markdown_formatting, switch_page, get_shopspace_logo

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
# Home button
col_a, col_b, col_c, col_d, col_e, col_f, col_g = st.columns([1,1,1,1,1,1,1])
home_button = col_a.button(label="Home", use_container_width=True)
if home_button:
    switch_page("sign_in_home")  

# Logo / Title
st.image(image=logo_image, use_column_width=True)
st.text(" ")
st.markdown("<h3 style='text-align: center; color: black;'>Safety Acknowlegement</h3>", unsafe_allow_html=True)
st.text(" ")
st.text(" ")

# Text
st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

# Buttons
col1, col2, col3 = st.columns([1,1,1])
acknowledge_safety_button = col2.button(label="I acknowledge the Safety Agreement", use_container_width=True)

if acknowledge_safety_button:
    switch_page("sia_choose_type")

