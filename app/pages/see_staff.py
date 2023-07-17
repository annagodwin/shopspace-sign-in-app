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
# Logo / Title
st.image(image=logo_image, use_column_width=True)
st.text(' ')
st.markdown("<h3 style='text-align: center; color: black;'>Please See a Staff Member</h3>", unsafe_allow_html=True)
st.text(' ')
st.text(' ')

# Conditional Text
if st.session_state.safety_class_status is False:
    safety_text = '- You have not completed the required safety class for Open Time.'
else:
    safety_text = None

if st.session_state.member_paid_status is False:
    paid_text = '- Your member dues for this month have not been paid.'
else:
    paid_text = None

# Message
st.markdown(f'The following errors were encountered for {st.session_state.type} Sign In for {st.session_state.first_name} {st.session_state.last_name} : ')
st.text(' ')
for t in [safety_text, paid_text]:
    if t is not None:
        st.markdown(t)
st.text(' ')
st.markdown('Please see a staff member.')

# Home Button
col1, col2, col3 = st.columns([1,1,1])
home_button = col2.button("Back to Sign-In Page", use_container_width=True)
if home_button:
    switch_page("sign_in_home")
