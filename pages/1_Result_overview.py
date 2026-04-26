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
s =stats.cursor()
st.subheader("Standings", anchor=False)
table = s.execute("""
SELECT name, wins, loses, wpoints, lpoints
FROM teams
ORDER BY wins DESC, wpoints DESC
""").fetchall()
df=pd.DataFrame(table,columns=["","Wins","Loses","Sets won", "Sets lost"])
st.table(df)
with st.container(horizontal=True):
    st.space("stretch")
    if st.button("Reload"):
        st.rerun()
