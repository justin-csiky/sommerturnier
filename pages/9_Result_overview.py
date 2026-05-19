import streamlit as st
import pandas as pd
import sqlite3
st.markdown("""
<style>
    [data-testid="stMainMenu"] {display: none;}
    [data-testid="stToolbarActions"] {display: none;}
    [data-testid="appCreatorAvatar"] {display: none;}
    [data-testid="manage-app-button"] {display: none;}
    footer {display: none;}
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
conn = sqlite3.connect("data.db",check_same_thread=False)
c = conn.cursor()
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
tab1, tab2, tab3 = st.tabs(["Gruppenphasen MX", "Gruppenphase LvL1/2", "Gruppenphase"])
if st.session_state.stt:
    mixedcon = st.expander("Mixed Tabelle", on_change="rerun")
    with mixedcon:
        table1 = c.execute("""
        SELECT name, wins, loses, wpoints, lpoints
        FROM teams WHERE class LIKE '%MX%'
        ORDER BY wins DESC, wpoints DESC
        """).fetchall()
        df1=pd.DataFrame(table1,columns=[":material/group: Team Name",":green[**Wins**]",":red[**Loses**]",":green[Sets won]", ":red[Sets lost]"])
        st.table(df1, border="horizontal")
    levelcon = st.expander("Level 1-2 Tabelle", on_change="rerun")
    with levelcon:
        table1 = c.execute("""
        SELECT name, wins, loses, wpoints, lpoints
        FROM teams WHERE class LIKE '%LVL1/2%'
        ORDER BY wins DESC, wpoints DESC
        """).fetchall()
        df1=pd.DataFrame(table1,columns=[":material/group: Team Name",":green[**Wins**]",":red[**Loses**]",":green[Sets won]", ":red[Sets lost]"])
        st.table(df1, border="horizontal")
    hdcon = st.expander("Herren Doppel Tabelle", on_change="rerun")
    with hdcon:
        table1 = c.execute("""
        SELECT name, wins, loses, wpoints, lpoints
        FROM teams WHERE class LIKE '%HD%'
        ORDER BY wins DESC, wpoints DESC
        """).fetchall()
        df1=pd.DataFrame(table1,columns=[":material/group: Team Name",":green[**Wins**]",":red[**Loses**]",":green[Sets won]", ":red[Sets lost]"])
        st.table(df1, border="horizontal")
    ddcon = st.expander("Damen Doppel Tabelle", on_change="rerun")
    with ddcon:
        table1 = c.execute("""
        SELECT name, wins, loses, wpoints, lpoints
        FROM teams WHERE class LIKE '%DD%'
        ORDER BY wins DESC, wpoints DESC
        """).fetchall()
        df1=pd.DataFrame(table1,columns=[":material/group: Team Name",":green[**Wins**]",":red[**Loses**]",":green[Sets won]", ":red[Sets lost]"])
        st.table(df1, border="horizontal")
matchdb = st.expander("matchesdb", on_change="rerun")
with matchdb:
    db = c.execute("""
    SELECT id, player1_id, player2_id, court, s1_p1, s1_p2, s2_p1, s2_p2, s3_p1, s3_p2, last_updated, is_new, is_visible, match_class
    FROM matches              
    """).fetchall()
    for i in db:
        st.markdown(i)
teamdb = st.expander("teamsdb", on_change="rerun")
with teamdb:
    db = c.execute("""
    SELECT id, name, wins, loses, wpoints, lpoints, class, team_group
    FROM teams
    """).fetchall()
    for i in db:
        st.markdown(i)
groupdb = st.expander("groupsdb", on_change="rerun")
with groupdb:
    db = c.execute("""
    SELECT id, class, group_name, is_done
    FROM groups
    """).fetchall()
    for i in db:
        st.markdown(i)