import streamlit as st
from utils.utilities import get_button_color_markdown_formatting, switch_page, get_shopspace_logo, get_error_log_df, get_daily_log_df, initialize_daily_log, initialize_error_log
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

# initialize dataframes if not created yet
# initialize log
daily_log_filepath = initialize_daily_log()
error_log_filepath = initialize_error_log()

# load dataframes
_, error_log_df = get_error_log_df()
_, daily_log_df = get_daily_log_df()

# split between signed in and signed out
daily_log_signed_in_df = daily_log_df[~daily_log_df['Sign Out Time'].notnull()]
daily_log_signed_out_df = daily_log_df[daily_log_df['Sign Out Time'].notnull()]

# on how to write df cell by cell to add a clickable button
# https://discuss.streamlit.io/t/make-streamlit-table-results-hyperlinks-or-add-radio-buttons-to-table/7883/12

# ===========
#     APP 
# ===========
# Initialize Session State
for key in st.session_state.keys():
    if 'admin_' in key:
        #TODO add sia_ prefix to sia-related keys
        del st.session_state[key]


# Logo / Title
st.image(image=logo_image, use_column_width=True)
st.text(' ')
st.markdown("<h3 style='text-align: center; color: black;'>Admin Home</h3>", unsafe_allow_html=True)
st.text(' ')
st.text(' ')

# # Signed In
st.markdown("### Signed In")
if len(daily_log_signed_in_df) == 0:
     st.markdown("No sign-in's yet today.")
else: 
    # temp table during dev
    # st.dataframe(daily_log_signed_in_df, hide_index=True)
    # create table with clickable button:
    signed_in_cols = ['Bookeo ID','First Name','Last Name','Type']
    user_table = daily_log_signed_in_df[signed_in_cols].copy(deep=True)
    colms = st.columns((1, 2, 2, 1, 1))
    fields = signed_in_cols + ['View']
    for col, field_name in zip(colms, fields):
        col.write(f"**{field_name}**")

    for x, bookeo_id in enumerate(user_table['Bookeo ID']):
        col1, col2, col3, col4, col5 = st.columns((1, 2, 2, 1, 1))
        col1.write(user_table['Bookeo ID'].iloc[x])  
        col2.write(user_table['First Name'].iloc[x])  
        col3.write(user_table['Last Name'].iloc[x])   
        col4.write(user_table['Type'].iloc[x])
        view_status = False  # flexible type of button
        button_type = "Viewing" if view_status else "View"
        button_phold = col5.empty()  # create a placeholder
        do_action = button_phold.button(button_type, key=x)
        if do_action:
                st.session_state.admin_bookeo_id = bookeo_id
                switch_page('admin_user_view')
                # pass # do some action with a row's data
                # button_phold.empty()  #  remove button
    # st.dataframe(daily_log_signed_in, hide_index=False)
    # # if click user name

# # Signed Out
st.markdown("### Signed Out")
if len(daily_log_signed_out_df) == 0:
     st.markdown("No sign-outs yet today.")
else: 
    sign_out_cols = ['Bookeo ID', 'First Name', 'Last Name', 'Phone Number', 'Type', 'Sign In Time', 'Sign Out Time']
    st.dataframe(daily_log_signed_out_df[sign_out_cols], hide_index=True)
# # TODO sign everyone out button --> go to page to confirm

# Error Signing In

st.markdown("### Error Log")
if len(error_log_df) == 0:
     st.markdown("No sign-outs yet today.")
else: 
    st.dataframe(error_log_df, hide_index=True)












