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

# generate lookup table


# ===========
#     APP 
# ===========
# Initialize Session State
for key in st.session_state.keys():
    del st.session_state[key]
st.session_state.type = None

# Logo / Title
st.image(image=logo_image, use_column_width=True)
st.text(' ')
st.markdown("<h3 style='text-align: center; color: black;'>Open Time Sign In</h3>", unsafe_allow_html=True)
st.text(' ')
st.text(' ')

# Buttons
col1, col2, col3, col4 = st.columns([1,1,1,1])
sign_in_button = col2.button(label="Sign In", use_container_width=True)
sign_out_button = col3.button(label="Sign Out", use_container_width=True)

if sign_in_button:
    switch_page("sia_safety_splash")

if sign_out_button:
    switch_page("sia_sign_out")


