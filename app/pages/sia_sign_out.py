import streamlit as st
import pandas as pd
from utils.utilities import get_button_color_markdown_formatting, switch_page, get_shopspace_logo, DEFAULT_SELECTION, selectbox, get_user_safety_status, get_user_paid_status, dedupe_and_order_list, get_daily_log_df
from pathlib import Path
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

# get data
daily_log_filepath, current_log_df = get_daily_log_df()
last_name_set = dedupe_and_order_list(current_log_df['Last Name'])

# ===========
#     APP 
# ===========
# Initialize state
st.session_state.safety_class_status = None
st.session_state.member_paid_status = None

# Home button
col_a, col_b, col_c, col_d, col_e, col_f, col_g = st.columns([1,1,1,1,1,1,1])
home_button = col_a.button(label="Home", use_container_width=True)
if home_button:
    switch_page("sign_in_home")  

# Logo / Title
st.image(image=logo_image, use_column_width=True)
st.text(" ")
st.markdown(f"<h3 style='text-align: center; color: black;'>Open Time Sign Out</h3>", unsafe_allow_html=True)
st.text(" ")
st.text(" ")

# TODO: I can't find my name, see a staff // Not doing this as of 7/16/23 chat with BB
st.markdown(f"Please select your Last Name")

selected_last_name = selectbox(
    "Last Name",
    last_name_set,
    no_selection_label=DEFAULT_SELECTION,
)

if selected_last_name:
    last_name_df = current_log_df.loc[(current_log_df['Last Name'] == selected_last_name)]

    if len(last_name_df) > 1:
        st.markdown(f"Please select your First Name")
        selected_first_name = selectbox(
            "First Name",
            dedupe_and_order_list(last_name_df['First Name']),
            no_selection_label=DEFAULT_SELECTION,
        )
        
        if selected_first_name: 
            first_last_name_df = last_name_df.loc[(last_name_df['First Name'] == selected_first_name)]


            if len(first_last_name_df) > 1:
                st.markdown(f"#### There's more than one membership entry for {selected_first_name} {selected_last_name}")
                st.markdown(f"Please choose the last 4 digits of your phone number:")

                first_last_name_df['Phone Number Last Four'] = first_last_name_df['Phone Number'].astype(str).str[-4:]
                selected_phone = selectbox(
                    "Last 4 digits of phone",
                    first_last_name_df['Phone Number Last Four'],
                    no_selection_label=DEFAULT_SELECTION,
                )

                if selected_phone:
                    user_df = first_last_name_df.loc[(first_last_name_df['Phone Number Last Four'] == selected_phone)]
                    sign_out_button_text = f'Sign out {selected_first_name} {selected_last_name} x{selected_phone}'

                else:
                    user_df = None
                    sign_out_button_text = None

    
            else: # first_name == 1
                user_df = first_last_name_df.copy(deep=True)
                sign_out_button_text = f'Sign out {selected_first_name} {selected_last_name}'
        
        else: # waiting for first name selection
            user_df = None
            sign_out_button_text = None
            
    else: # last_name == 1
        user_df = last_name_df.copy(deep=True)
        first_name = user_df['First Name'].iloc[0]
        sign_out_button_text = f'Sign out {first_name} {selected_last_name}'


    if user_df is not None:
        # User Details to session state (alongside Type)
        bookeo_id = user_df['Bookeo ID'].iloc[0]
        sign_out_time = datetime.now().strftime('%H:%M')

        sign_out_button = st.button(sign_out_button_text)

        if sign_out_button:
            
            daily_log_df = pd.read_csv(daily_log_filepath)

            # filter to user record
            user_row_df = daily_log_df.loc[(daily_log_df['Bookeo ID'] == bookeo_id)]
            user_row_df['Sign Out Time'] = sign_out_time

            # everything but the user record
            updated_daily_log_df = daily_log_df[~(daily_log_df['Bookeo ID'] == bookeo_id)]
            updated_daily_log_df = pd.concat([updated_daily_log_df, user_row_df])
            updated_daily_log_df.to_csv(daily_log_filepath, index=False)

            switch_page("sia_thank_you")

