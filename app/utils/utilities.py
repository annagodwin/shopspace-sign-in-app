import streamlit as st
from streamlit.runtime.scriptrunner import RerunData, RerunException
from streamlit.source_util import get_pages
from PIL import Image
from pathlib import Path
import pandas as pd
from typing import Any, Iterable
from datetime import datetime
import os

def get_shopspace_logo():
    im = Image.open(Path('resources/logo/ShopSpace-YellowLogo1200x320.png'))
    return im 

# === PAGE SETTINGS ===

def get_button_color_markdown_formatting():

    # button base color formatting & on hover formatting
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

    return m


# SWITCH PAGE BUTTON ===
def switch_page(page_name: str):

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("src/app/sign_in_home.py")  # OR whatever your main page is called

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
def dedupe_and_order_list(input_list):
    return sorted(list(set(list(input_list))), key=str.lower)


@st.cache_data
def load_name_set(data_path, col_name):
    members_df = pd.read_csv(data_path) 

    # list, set, list - deduplicates entries for the drop down list
    members_name_set = sorted(list(set(list(members_df[col_name]))), key=str.lower)

    return members_name_set


@st.cache_data
def lookup_users_details_df(data_path):
    members_df = pd.read_csv(data_path)
    return members_df


def get_user_safety_status(b_id):
    safety_path = Path('resources/sign_in_app/open_time_safety_class_list.csv')
    df = pd.read_csv(safety_path)
    user_df = df.loc[(df['Bookeo ID'] == b_id)]

    if len(user_df) == 1:
        safety_bool = True
    else: 
        safety_bool = False
    
    return safety_bool

def get_user_paid_status(b_id):
    members_path = Path('resources/sign_in_app/membership_list.csv')
    df = pd.read_csv(members_path)
    user_df = df.loc[(df['Bookeo ID'] == b_id)]
    paid_check = user_df['Member Paid Up'].iloc[0]
    
    if paid_check == 'F':
        paid_bool = False

    if paid_check == 'T':   
        paid_bool = True
    
    return paid_bool


# INITIALIZE LOG
def initialize_daily_log() -> Path:
    log_path = Path("resources/sign_in_app/")
    julian_date = datetime.now().strftime('%Y%m%d') 
    log_filename = Path(f'{julian_date}_sign_in_log.csv')
    log_filepath = log_path / log_filename
    
    if not os.path.exists(log_filepath):
        daily_log_df=pd.DataFrame(columns=['Bookeo ID','First Name','Last Name','Phone Number','Type','Member Paid Status','Safety Class Status','Sign In Time','Sign Out Time'])
        daily_log_df.to_csv(log_filepath,index=False)
    
    return log_filepath

def initialize_error_log(clear_log=False) -> Path:
    log_path = Path("resources/sign_in_app/")
    julian_date = datetime.now().strftime('%Y%m%d') 
    log_filename = Path(f'{julian_date}_sign_in_error_log.csv')
    log_filepath = log_path / log_filename
    
    if not os.path.exists(log_filepath):
        df=pd.DataFrame(columns=['Bookeo ID','First Name','Last Name','Phone Number','Type','Member Paid Status','Safety Class Status','Sign In Time','Sign Out Time'])
        df.to_csv(log_filepath,index=False)
    
    if clear_log is True:
        df=pd.DataFrame(columns=['Bookeo ID','First Name','Last Name','Phone Number','Type','Member Paid Status','Safety Class Status','Sign In Time','Sign Out Time'])
        df.to_csv(log_filepath,index=False)
    
    return log_filepath

def get_daily_log_df():
    log_path = Path("resources/sign_in_app/")
    julian_date = datetime.now().strftime('%Y%m%d') 
    log_filename = Path(f'{julian_date}_sign_in_log.csv')
    log_filepath = log_path / log_filename
    
    df = pd.read_csv(log_filepath)
    
    return log_filepath, df

def get_error_log_df():
    log_path = Path("resources/sign_in_app/")
    julian_date = datetime.now().strftime('%Y%m%d') 
    log_filename = Path(f'{julian_date}_sign_in_error_log.csv')
    log_filepath = log_path / log_filename
    
    df = pd.read_csv(log_filepath)
    
    return log_filepath, df


def get_tool_training_df(b_id):
    log_path = Path("resources/sign_in_app/tool_training_list.csv")
    
    df = pd.read_csv(log_path)
    
    output_df = df[df['Bookeo ID'] == b_id]
    
    return output_df



def get_notes_df(b_id):
    log_path = Path("resources/sign_in_app/user_notes_list.csv")
    
    df = pd.read_csv(log_path)
    
    output_df = df[df['Bookeo ID'] == b_id]
    
    return output_df
