import streamlit as st
from utils.utilities import get_button_color_markdown_formatting, switch_page, get_shopspace_logo, get_daily_log_df, get_tool_training_df, get_notes_df
import pandas as pd


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
# _, error_log_df = get_error_log_df()
_, daily_log_df = get_daily_log_df()

# load/subset dataframes
user_log_df = daily_log_df[daily_log_df['Bookeo ID'] == st.session_state.admin_bookeo_id]
user_tool_training_df = get_tool_training_df(st.session_state.admin_bookeo_id)
user_notes_df = get_notes_df(st.session_state.admin_bookeo_id)


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
st.markdown("<h3 style='text-align: center; color: black;'>Individual View</h3>", unsafe_allow_html=True)
st.text(' ')

# User Name Header
first_name = user_log_df['First Name'].iloc[0]
last_name = user_log_df['Last Name'].iloc[0]
st.markdown(f"<h2 style='text-align: center; color: black;'>{first_name} {last_name}</h2>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align: center; color: black;'>Bookeo ID {st.session_state.admin_bookeo_id}</h4>", unsafe_allow_html=True)


# Signed In
st.markdown("### Signed In Details")
st.dataframe(user_log_df, hide_index=True)

# Tool Status
st.markdown("### Tool Training Stats")
if len(user_tool_training_df) == 0:
    st.markdown(f'No tool specific trainings for {first_name} {last_name}.')
else:
    tool_cols = ['Tool Name','Training Date','Trainer']
    st.dataframe(user_tool_training_df[tool_cols], hide_index=True)

# Notes
st.markdown("### Notes")
if len(user_notes_df) == 0:
    st.markdown(f'No notes for {first_name} {last_name}.')
else:
    for note in list(user_notes_df['Note']):
        st.markdown(f'- {note}')

