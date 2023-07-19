import streamlit as st
import pandas as pd
from utils.utilities import get_button_color_markdown_formatting, switch_page, get_shopspace_logo, load_name_set, lookup_users_details_df, DEFAULT_SELECTION, selectbox, initialize_daily_log, get_user_safety_status, get_user_paid_status, dedupe_and_order_list, initialize_error_log
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

if st.session_state.type == 'Member':
    data_fpath = Path('resources/sign_in_app/membership_list.csv')
else: #elif hourly then else fail
    data_fpath = Path('resources/sign_in_app/open_time_safety_class_list.csv')

last_name_set = load_name_set(data_fpath, 'Last Name')
users_details_df = lookup_users_details_df(data_fpath)

# initialize log
daily_log_filepath = initialize_daily_log()
error_log_filepath = initialize_error_log()

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
st.markdown(f"<h3 style='text-align: center; color: black;'>{st.session_state.type} Sign In</h3>", unsafe_allow_html=True)
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
    last_name_df = users_details_df.loc[(users_details_df['Last Name'] == selected_last_name)]

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
                    sign_in_button_text = f'Sign in {selected_first_name} {selected_last_name} x{selected_phone}'

                else:
                    user_df = None
                    sign_in_button_text = None

    
            else: # first_name == 1
                user_df = first_last_name_df.copy(deep=True)
                sign_in_button_text = f'Sign in {selected_first_name} {selected_last_name}'
        
        else: # waiting for first name selection
            user_df = None
            sign_in_button_text = None
            
    else: # last_name == 1
        user_df = last_name_df.copy(deep=True)
        first_name = user_df['First Name'].iloc[0]
        sign_in_button_text = f'Sign in {first_name} {selected_last_name}'


    if user_df is not None:
        # User Details to session state (alongside Type)
        st.session_state.bookeo_id = user_df['Bookeo ID'].iloc[0]
        st.session_state.first_name = user_df['First Name'].iloc[0]
        st.session_state.last_name = user_df['Last Name'].iloc[0]
        st.session_state.phone_number = user_df['Phone Number'].iloc[0]

        if st.session_state.type == 'Member':
            
            st.session_state.member_paid_status = get_user_paid_status(st.session_state.bookeo_id)
            st.session_state.safety_class_status = get_user_safety_status(st.session_state.bookeo_id)
        
        elif st.session_state.type == 'Hourly':
            st.session_state.safety_class_status = get_user_safety_status(st.session_state.bookeo_id)
            st.session_state.member_paid_status = 'N/A'

        sign_in_time = datetime.now().strftime('%H:%M')
        sign_in_user_df = pd.DataFrame([{'Bookeo ID': st.session_state.bookeo_id,
                                        'First Name': st.session_state.first_name,
                                        'Last Name': st.session_state.last_name,
                                        'Phone Number': st.session_state.phone_number,
                                        'Type': st.session_state.type,
                                        'Member Paid Status': st.session_state.member_paid_status,
                                        'Safety Class Status': st.session_state.safety_class_status,
                                        'Sign In Time': sign_in_time,
                                        'Sign Out Time': ''}])


        if (st.session_state.member_paid_status is False) | (st.session_state.safety_class_status is False):

            error_log_df = pd.read_csv(error_log_filepath)
            error_log_df = pd.concat([error_log_df, sign_in_user_df])
            error_log_df.to_csv(error_log_filepath, index=False)
            
            switch_page("sia_see_staff")


        sign_in_button = st.button(sign_in_button_text)

        if sign_in_button:
            
            daily_log_df = pd.read_csv(daily_log_filepath)
            daily_log_df = pd.concat([daily_log_df, sign_in_user_df])
            daily_log_df.to_csv(daily_log_filepath, index=False)

            switch_page("sia_thank_you")

