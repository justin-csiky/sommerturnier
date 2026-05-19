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
def close_group():
    st.warning("Noch nicht hinzugefügt")
    return 0
def print_table(r,group):
    h1, h2, h3, h4 = st.columns([5,1,1,2])
    h1.markdown(":blue[:material/group: **Team Name**]")
    h2.markdown("<div style='text-align:center'><p style='color: #21c354;'><b>W</b></p></div>", unsafe_allow_html=True)
    h3.markdown("<div style='text-align:center'><p style='color: #ff4b4b;'><b>L</b></p></div>", unsafe_allow_html=True)
    h4.markdown("<div style='text-align:center'><p style='color: #1c83e0;'><b>Set +/-</b></p></div>", unsafe_allow_html=True)
    table1=[]
    for i in r:
        if i[5]==group:
            table1.append([i[0],i[1],i[2],f"{i[3]} : {i[4]}"])
    if table1==[]:
        with st.container(horizontal=True):
            st.space("stretch")
            st.markdown(":gray[Turnierleitung erstellt Gruppe...]")
            st.space("stretch")
    else:
        for name, wins, losses, diff in table1:
            c1, c2, c3, c4 = st.columns([5,1,1,2])
            c1.markdown(
                f"<div><p style='margin:0; line-height:1.5'>{name}</p></div>",
                unsafe_allow_html=True
            )
            c2.markdown(
                f"<div style='text-align:center'><p style='margin:0; line-height:1.5'>{wins}</p></div>",
                unsafe_allow_html=True
            )
            c3.markdown(
                f"<div style='text-align:center'><p style='margin:0; line-height:1.5'>{losses}</p></div>",
                unsafe_allow_html=True
            )
            c4.markdown(
                f"<div style='text-align:center'><p style='margin:0; line-height:1.5'>{diff}</p></div>",
                unsafe_allow_html=True
            )
        c1, c2, c3, c4 = st.columns([5,1,1,2])
        c1.space("stretch")
    return 0
def finish_group(gname):
    klassengruppe = c.execute("SELECT id, group_name FROM groups WHERE class=?", ('HD',)).fetchall()
    for i in klassengruppe:
        tid, name = i
        if name==gname:
            c.execute("UPDATE groups SET is_done=? WHERE id=?",(1,tid))
            conn.commit()  
    return 0
if "admin" not in st.session_state:
    st.session_state.admin = False
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None
if "stt" not in st.session_state:
    st.session_state.stt = False
st.subheader("Herren Doppel Turnier", anchor=False)
tab1, tab2, tab3, tab4 = st.tabs(["Gruppenphase", "Viertelfinale", "Halbfinale", "Finale"])
with tab1:
    grA = st.expander("Gruppe A", on_change="rerun",key="gruppeA")
    with grA:
        raw = c.execute("""
        SELECT name, wins, loses, wpoints, lpoints, team_group
        FROM teams WHERE class LIKE '%HD%'
        ORDER BY wins DESC, wpoints DESC
        """).fetchall()
        print_table(raw,'A')
        if st.session_state.admin:
            with st.container(horizontal=True):
                st.space("stretch")
                if st.button("Gruppe abschließen",width=200,key="bt_gruppeA"):
                    finish_group('A')   
                st.space("stretch")
    grB = st.expander("Gruppe B", on_change="rerun",key="gruppeB")
    with grB:
        raw = c.execute("""
        SELECT name, wins, loses, wpoints, lpoints, team_group
        FROM teams WHERE class LIKE '%HD%'
        ORDER BY wins DESC, wpoints DESC
        """).fetchall()
        print_table(raw,'B')
        if st.session_state.admin:
            with st.container(horizontal=True):
                st.space("stretch")
                if st.button("Gruppe abschließen",width=200,key="bt_gruppeB"):
                    finish_group('B')     
                st.space("stretch")
    grC = st.expander("Gruppe C", on_change="rerun",key="gruppeC")
    with grC:
        raw = c.execute("""
        SELECT name, wins, loses, wpoints, lpoints, team_group
        FROM teams WHERE class LIKE '%HD%'
        ORDER BY wins DESC, wpoints DESC
        """).fetchall()
        print_table(raw,'C')
        if st.session_state.admin:
            with st.container(horizontal=True):
                st.space("stretch")
                if st.button("Gruppe abschließen",width=200,key="bt_gruppeC"):
                    finish_group('C')     
                st.space("stretch")
    grD = st.expander("Gruppe D", on_change="rerun",key="gruppeD")
    with grD:
        raw = c.execute("""
        SELECT name, wins, loses, wpoints, lpoints, team_group
        FROM teams WHERE class LIKE '%HD%'
        ORDER BY wins DESC, wpoints DESC
        """).fetchall()
        print_table(raw,'D')
        if st.session_state.admin:
            with st.container(horizontal=True):
                st.space("stretch")
                if st.button("Gruppe abschließen",width=200,key="bt_gruppeD"):
                    finish_group('D')     
                st.space("stretch")