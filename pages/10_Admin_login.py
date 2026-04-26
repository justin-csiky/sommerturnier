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
state_change = "admin123"
st.header("Admin Login",anchor=False)
if not st.session_state.admin:
    input = st.text_input("Password", type="password",width=300)
    if st.button("Login"):
        if input == state_change:
            st.session_state.admin = True
            st.rerun()
        else:
            st.error("Wrong password")
if st.session_state.admin:
    st.success("Currently logged in")
    if st.button("Logout"):
        st.session_state.admin = False
        st.rerun()