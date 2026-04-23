import streamlit as st
import sqlite3
st.markdown("""
<style>
    /* Hide top header, hamburger menu, and footer */
    [data-testid="stMainMenu"] {display: none;}
    [data-testid="stToolbarActions"] {display: none;}
    [data-testid="appCreatorAvatar"] {display: none;}
</style>
""", unsafe_allow_html=True)
stats = sqlite3.connect("stats.db",check_same_thread=False)
s =stats.cursor()
st.subheader("Team list", anchor=False)
teams = s.execute("""
    SELECT id, name, wins, loses, wpoints, lpoints
    FROM teams
""").fetchall()
for team in teams:
    team_id, team_name, w, l, wp, lp = team
    with st.container(horizontal=True):
        st.write(team_name)
        if st.session_state.admin:
            if st.button("🗑️",key=f"del_{team_id}",width=50):
                s.execute("DELETE FROM teams WHERE id=?", (team_id,))
                stats.commit()
                st.rerun()
