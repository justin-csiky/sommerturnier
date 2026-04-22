import streamlit as st
import time
import sqlite3
from datetime import datetime
ADMIN_PASSWORD = "admin123"

st.header("Admin Login",anchor=False)
if not st.session_state.admin:
    password = st.text_input("Password", type="password",width=300)
    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state.admin = True
            st.rerun()

        else:
            st.error("Wrong password")

if st.session_state.admin:
    st.success("Currently logged in")
    if st.button("Logout"):
        st.session_state.admin = False
        st.rerun()