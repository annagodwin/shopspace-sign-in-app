import streamlit as st
import pandas as pd
from pathlib import Path
from utils.utilities import get_button_color_markdown_formatting, switch_page, get_shopspace_logo, selectbox, DEFAULT_SELECTION


# ===========
#    SETUP 
# ===========

# sidebar config
st.set_page_config(initial_sidebar_state="collapsed")

# button config
m = get_button_color_markdown_formatting()

# load assets
logo_image = get_shopspace_logo()
# members_dataset = load_members_set(Path('resources/sign_in_app/members.csv'))


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
st.text(' ')
st.markdown("<h3 style='text-align: center; color: black;'>Open Time Sign Out</h3>", unsafe_allow_html=True)
st.text(' ')
st.text(' ')

# Message / Selectbox
st.markdown("Begin typing your Last Name or scroll to select your name below")


# selected_name = selectbox(
#     "Last Name, First Name",
#     members_dataset,
#     no_selection_label=DEFAULT_SELECTION,
# )

# if selected_name:
#     # st.text(" ")
#     # st.text(" ")

#     st.markdown("## Selection Confirmation")
#     st.text(" ")
#     st.markdown("You selected:")
#     st.markdown(f"#### {selected_name}")

#     st.text(" ")
#     st.markdown("Is this correct?")

#     st.text(" ")
#     correct_button = st.button("Correct! Sign me in")

#     if correct_button:
#         switch_page("thank_you")

