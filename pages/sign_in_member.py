import streamlit as st
from streamlit.runtime.scriptrunner import RerunData, RerunException
from streamlit.source_util import get_pages
import pandas as pd
from pathlib import Path
from PIL import Image
from typing import Any, Iterable
from datetime import datetime
import os
import time

# === PAGE SETTINGS === 
# disable sidebar
st.set_page_config(initial_sidebar_state="collapsed")

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #F7D47F;
    color:black;
}
div.stButton > button:hover {
    background-color: #F7AD2F;
    color:black;
    }
</style>
""", unsafe_allow_html=True)

# === from streamlit extras ===

def switch_page(page_name: str):

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("home.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")


def _transform_arguments(*args, **kwargs) -> tuple[str, Iterable[Any], dict[str, Any]]:
    no_selection_label = kwargs.pop("no_selection_label", "---")

    _args = list(args)

    # Get the options from either the args or kwargs
    try:
        options = _args.pop(1)
    except IndexError:
        options = kwargs["options"]

    # Prepend the no-selection option to the list of options
    if no_selection_label not in options:
        if isinstance(options, pd.Series):
            options = list(pd.concat([pd.Series([no_selection_label]), options]))
        elif isinstance(options, pd.DataFrame):
            # If the options are a DataFrame, the options are just the first column
            options = options.iloc[:, 0]
            options = list(pd.concat([pd.Series([no_selection_label]), options]))
        else:
            options = [no_selection_label] + list(options)
        kwargs["options"] = options

    return no_selection_label, _args, kwargs


def selectbox(*args, **kwargs):
    """A selectbox that returns None unless the user has explicitly selected one of the
    options.
    All arguments are passed to st.selectbox except for `no_selection_label`, which is
    used to specify the label of the option that represents no selection.
    Parameters
    ----------
    no_selection_label : str
        The label to use for the no-selection option. Defaults to "---".
    """
    no_selection_label, _args, _kwargs = _transform_arguments(*args, **kwargs)

    result = st.selectbox(*_args, **_kwargs)
    if result == no_selection_label:
        return None
    return result


DEFAULT_SELECTION = ""

# === CACHE FUNCTIONS ===
@st.cache_data
def load_members_name_set(data_path):

    members_df = pd.read_csv(data_path) 
    members_df['Name List'] = members_df["Last Name"] + ", " + members_df["First Name"]

    # list, set, list - deduplicates entries for the drop down list
    members_name_set = sorted(list(set(list(members_df["Name List"]))), key=str.lower)

    return members_name_set

@st.cache_data
def lookup_member_details_df(data_path):
    members_df = pd.read_csv(data_path)
    return members_df




# === LOAD ASSETS ===
logo_image = Image.open(Path('resources/logo/ShopSpace-YellowLogo1200x320.png'))

members_name_set = load_members_name_set(Path('resources/sign_in_app/membership_list.csv'))
members_details_df = lookup_member_details_df(Path('resources/sign_in_app/membership_list.csv'))

log_path = Path("/Users/akgodwin/Repos/Github_annagodwin/shopspace-sign-in-app/resources/sign_in_app/")
julian_date = datetime.now().strftime('%Y%m%d') 
log_filename = Path(f'{julian_date}_sign_in_log.csv')
log_filepath = log_path / log_filename
if not os.path.exists(log_filepath):
    daily_log_df=pd.DataFrame(columns=['Bookeo ID', 'First Name','Last Name','Sign In Time', 'Sign Out Time'])
    daily_log_df.to_csv(log_filepath,index=False)


# === APP ===
# Image
st.image(image=logo_image, use_column_width=True)

st.title("Member Sign-In")

st.markdown("Begin typing your Last Name or scroll to select your name below")

# TODO: I can't find my name, see a staff // Not doing this as of 7/16/23 chat with BB
selected_name = selectbox(
    "Last Name, First Name",
    members_name_set,
    no_selection_label=DEFAULT_SELECTION,
)

if selected_name:

    st.text(" ")
    first_name = selected_name.split(', ')[1]
    last_name = selected_name.split(', ')[0]

    member_info_df = members_details_df.loc[(members_details_df['First Name'] == first_name) & (members_details_df['Last Name'] == last_name)]

    if len(member_info_df) > 1:
        # if there's more than 1 member

        st.markdown(f"#### There's more than one membership entry for {first_name} {last_name}")

        st.markdown(f"Please choose the last 4 digits of your phone number:")

        member_info_df['Phone Number Last Four'] = member_info_df['Phone Number'].astype(str).str[-4:]
        selected_phone = selectbox(
            "Last 4 digits of phone",
            member_info_df['Phone Number Last Four'],
            no_selection_label=DEFAULT_SELECTION,
        )

        if selected_phone: 

            member_info_df = member_info_df.loc[(member_info_df['Phone Number Last Four'] == selected_phone)]
            # TODO: Check if paid-up
            # TODO: Check if safety class

            sign_in_time = datetime.now().strftime('%H:%M')
            bookeo_id = member_info_df['Bookeo ID'].iloc[0] 
            sign_in_member_df = pd.DataFrame(
                                [{'Bookeo ID': bookeo_id,
                                'First Name': first_name,
                                'Last Name': last_name,
                                'Sign In Time': sign_in_time,
                                'Sign Out Time': ''}])
            
            correct_button = st.button(f"Sign in {first_name} {last_name} x{selected_phone}")
        else:
            correct_button = None

    else:
        
        # TODO: Check if paid-up
        # TODO: Check if safety class

        sign_in_time = datetime.now().strftime('%H:%M')
        bookeo_id = member_info_df['Bookeo ID'].iloc[0] 
        sign_in_member_df = pd.DataFrame(
                            [{'Bookeo ID': bookeo_id,
                            'First Name': first_name,
                            'Last Name': last_name,
                            'Sign In Time': sign_in_time,
                            'Sign Out Time': ''}])
        
        correct_button = st.button(f"Sign in {first_name} {last_name}")



    if correct_button:
        # TODO: Check if name is already signed in

        daily_log_df = pd.read_csv(log_filepath)
        daily_log_df = pd.concat([daily_log_df, sign_in_member_df])
        daily_log_df.to_csv(log_filepath, index=False)

        switch_page("thank_you")

