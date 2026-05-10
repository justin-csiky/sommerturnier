import streamlit as st
import pandas as pd
import sqlite3
st.markdown("""
<style>
    /* Hide top header, hamburger menu, and footer */
    [data-testid="stMainMenu"] {display: none;}
    [data-testid="stToolbarActions"] {display: none;}
    [data-testid="appCreatorAvatar"] {display: none;}
</style>
""", unsafe_allow_html=True)
stats = sqlite3.connect("teamstats.db",check_same_thread=False)
s = stats.cursor()
st.subheader("Standings", anchor=False)
with st.container(horizontal=True):
    if st.session_state.stt:
        if st.button("Gruppenphase",width=150):
            st.session_state.stt=False
            st.rerun()
    else:
        if st.button("Tabellen",width=150):
            st.session_state.stt=True
            st.rerun()
    st.space("stretch")
    if st.button(":material/refresh: Reload",width=100):
        st.rerun()
if st.session_state.stt:
    mixedcon = st.expander("Mixed Tabelle", on_change="rerun")
    with mixedcon:
        table1 = s.execute("""
        SELECT name, wins, loses, wpoints, lpoints
        FROM teams WHERE class LIKE '%MX%'
        ORDER BY wins DESC, wpoints DESC
        """).fetchall()
        df1=pd.DataFrame(table1,columns=[":material/group: Team Name",":green[**Wins**]",":red[**Loses**]",":green[Sets won]", ":red[Sets lost]"])
        st.table(df1, border="horizontal")
    levelcon = st.expander("Level 1-2 Tabelle", on_change="rerun")
    with levelcon:
        table1 = s.execute("""
        SELECT name, wins, loses, wpoints, lpoints
        FROM teams WHERE class LIKE '%LVL1/2%'
        ORDER BY wins DESC, wpoints DESC
        """).fetchall()
        df1=pd.DataFrame(table1,columns=[":material/group: Team Name",":green[**Wins**]",":red[**Loses**]",":green[Sets won]", ":red[Sets lost]"])
        st.table(df1, border="horizontal")
    hdcon = st.expander("Herren Doppel Tabelle", on_change="rerun")
    with hdcon:
        table1 = s.execute("""
        SELECT name, wins, loses, wpoints, lpoints
        FROM teams WHERE class LIKE '%HD%'
        ORDER BY wins DESC, wpoints DESC
        """).fetchall()
        df1=pd.DataFrame(table1,columns=[":material/group: Team Name",":green[**Wins**]",":red[**Loses**]",":green[Sets won]", ":red[Sets lost]"])
        st.table(df1, border="horizontal")
    ddcon = st.expander("Damen Doppel Tabelle", on_change="rerun")
    with ddcon:
        table1 = s.execute("""
        SELECT name, wins, loses, wpoints, lpoints
        FROM teams WHERE class LIKE '%DD%'
        ORDER BY wins DESC, wpoints DESC
        """).fetchall()
        df1=pd.DataFrame(table1,columns=[":material/group: Team Name",":green[**Wins**]",":red[**Loses**]",":green[Sets won]", ":red[Sets lost]"])
        st.table(df1, border="horizontal")
