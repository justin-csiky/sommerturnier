import streamlit as st
import time
import sqlite3
from datetime import datetime
ADMIN_PASSWORD = "admin123"

st.header("Admin Login")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if password == ADMIN_PASSWORD:
        st.session_state.admin = True
        st.success("Logged in")
    else:
        st.error("Wrong password")

if st.session_state.admin:
    if st.button("Logout"):
        st.session_state.admin = False