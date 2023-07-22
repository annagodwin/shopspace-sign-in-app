import streamlit as st
from utils.utilities import get_button_color_markdown_formatting, switch_page, get_shopspace_logo, get_error_log_df, get_daily_log_df, initialize_daily_log, initialize_error_log
import pandas as pd
from datetime import datetime


# ===========
#    SETUP 
# ===========
# sidebar config
st.set_page_config(initial_sidebar_state="collapsed")

# button config
m = get_button_color_markdown_formatting()

# load assets
logo_image = get_shopspace_logo()

# load dataframes
daily_log_path, daily_log_df = get_daily_log_df()


# ===========
#     APP 
# ===========
# Home button
col_a, col_b, col_c, col_d, col_e, col_f, col_g = st.columns([1,1,1,1,1,1,1])
home_button = col_a.button(label="Admin Home", use_container_width=True)
if home_button:
    switch_page("admin_home") 

# Logo / Title
st.image(image=logo_image, use_column_width=True)
st.text(' ')
st.markdown("<h3 style='text-align: center; color: black;'>Sign Out Everyone</h3>", unsafe_allow_html=True)
st.text(' ')
st.text(' ')

st.markdown("Are you sure you want to clear the error log?")

st.text(' ')
st.text(' ')

col_a, col_b, col_c = st.columns([1,1,1])
clear_error_log_button = col_b.button("Yes, sign out everyone")

if clear_error_log_button:
    col_b.write('')

    initialize_error_log(clear_log=True)

    st.markdown("The error log has been cleared.")

