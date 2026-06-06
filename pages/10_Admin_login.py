import streamlit as st
import time
import sqlite3
from datetime import datetime
st.markdown("""
<style>
    /* Hide top header, hamburger menu, and footer */
    [data-testid="stMainMenu"] {display: none;}
    [data-testid="stToolbarActions"] {display: none;}
    [data-testid="appCreatorAvatar"] {display: none;}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
    /* Hide bottom-right floating button */
    button[kind="header"] {
        visibility: hidden;
    }

    /* Extra fallback selectors */
    [data-testid="stStatusWidget"] {
        display: none;
    }

    .stDeployButton {
        display: none;
    }
</style>
""", unsafe_allow_html=True)
state_change = "admin123"
if "admin" not in st.session_state:
    st.session_state.admin = False
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None
if "language" not in st.session_state:
    st.session_state.language = "german"
if "input_mode" not in st.session_state:
    st.session_state.input_mode = False
with st.container(horizontal=True):
    if st.button("🇩🇪"):
        st.session_state.language="german"
        st.rerun()
    if st.button("🇬🇧"):
        st.session_state.language="english"
        st.rerun()
    st.space("stretch")
    if st.session_state.admin:
        if st.button(":material/logout: Logout",width=100):
            st.session_state.admin = False
            st.session_state.input_mode = False
            st.rerun()
    if st.button(":material/refresh: Reload",width=100):
        st.rerun()
if st.session_state.admin:
    st.subheader(":green[Logged in]",anchor=False)
    if st.session_state.input_mode:
        if st.checkbox("Input Modus aus"):
            st.session_state.input_mode = False
            st.rerun()
    else:
        if st.checkbox("Input Modus an"):
            st.session_state.input_mode = True
            st.rerun()
else:
    st.subheader("Admin Login",anchor=False)
    input = st.text_input("Password", type="password",label_visibility="collapsed",width=300)
    if st.button(":material/login: Login",width=100):
        if input == state_change:
            st.session_state.admin = True
            st.rerun()
        else:
            st.error("Wrong password")