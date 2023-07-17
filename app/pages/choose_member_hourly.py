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
col1, col2, col3 = st.columns([0.25,0.5,0.25])
col2.markdown("<h3 style='text-align: center; color: black;'>Choose Open Time Type</h3>", unsafe_allow_html=True)
col2.text(" ")
col2.text(" ")


# Buttons
col1, col2, col3, col4 = st.columns([1,1,1,1])
sign_in_member_button = col2.button(label="Member", use_container_width=True)
sign_in_hourly_button = col3.button(label="Hourly", use_container_width=True)

if sign_in_member_button:
    st.session_state.type = 'Member'
    switch_page("sign_in")

if sign_in_hourly_button:
    st.session_state.type = 'Hourly'
    switch_page("sign_in")



