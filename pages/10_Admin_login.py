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
st.subheader("Admin Login",anchor=False)
if not st.session_state.admin:
    input = st.text_input("Password", type="password",label_visibility="collapsed",width=300)
    if st.button(":material/login: Login",width=100):
        if input == state_change:
            st.session_state.admin = True
            st.rerun()
        else:
            st.error("Wrong password")
if st.session_state.admin:
    st.success(":material/Check: Currently logged in",width=200)
    if st.button(":material/logout: Logout",width=100):
        st.session_state.admin = False
        st.rerun()