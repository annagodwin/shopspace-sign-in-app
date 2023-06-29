import streamlit as st
from streamlit.runtime.scriptrunner import RerunData, RerunException
from streamlit.source_util import get_pages
import pandas as pd
from pathlib import Path
from PIL import Image
from typing import Any, Iterable

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

    pages = get_pages("src/sign_in_app/home.py")  # OR whatever your main page is called

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
def load_members_set(data_path):

    members_df = pd.read_csv(data_path) 
    members_df['Name List'] = members_df["Last Name"] + ", " + members_df["First Name"]
    members_set = list(members_df["Name List"].sort_values(key=lambda x: x.str.lower()))
    
    return members_set


# === LOAD ASSETS ===
logo_image = Image.open(Path('resources/logo/ShopSpace-YellowLogo1200x320.png'))
members_dataset = load_members_set(Path('resources/sign_in_app/members.csv'))


# === APP ===
# Image
st.image(image=logo_image, use_column_width=True)

st.title("Member Sign-In")

st.markdown("Begin typing your Last Name or scroll to select your name below")


selected_name = selectbox(
    "Last Name, First Name",
    members_dataset,
    no_selection_label=DEFAULT_SELECTION,
)

if selected_name:
    # st.text(" ")
    # st.text(" ")

    st.markdown("## Selection Confirmation")
    st.text(" ")
    st.markdown("You selected:")
    st.markdown(f"#### {selected_name}")

    st.text(" ")
    st.markdown("Is this correct?")

    st.text(" ")
    correct_button = st.button("Correct! Sign me in")

    if correct_button:
        switch_page("thank_you")

