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
def parse_to_int(v):
    try:
        return int(v)
    except:
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
    groupid = c.execute("SELECT id, class FROM groups WHERE class=? and group_name=?", ('LVL1/2',gname)).fetchone()
    c.execute("UPDATE groups SET is_done=? WHERE id=?",(1,groupid[0]))
    teams = c.execute("SELECT id FROM teams WHERE class=? and team_group=? ORDER BY wins DESC, wpoints DESC", ('LVL1/2',gname)).fetchall()
    placement = 1
    for i in teams:
        id = i[0]
        c.execute("UPDATE teams SET group_placement=? WHERE id=?",(placement,id))
        placement+=1
    conn.commit()  
    return 0
if "admin" not in st.session_state:
    st.session_state.admin = False
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None
if "stt" not in st.session_state:
    st.session_state.stt = False
st.subheader("Level 1-2 Turnier", anchor=False)
tab1, tab2, tab3, tab4 = st.tabs(["Gruppenphase", "Viertelfinale", "Halbfinale", "Finale"])
with tab1:
    grA = st.expander("Gruppe A", on_change="rerun",key="gruppeA")
    with grA:
        raw = c.execute("""
        SELECT name, wins, loses, wpoints, lpoints, team_group
        FROM teams WHERE class LIKE '%LVL1/2%'
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
        FROM teams WHERE class LIKE '%LVL1/2%'
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
        FROM teams WHERE class LIKE '%LVL1/2%'
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
        FROM teams WHERE class LIKE '%LVL1/2%'
        ORDER BY wins DESC, wpoints DESC
        """).fetchall()
        print_table(raw,'D')
        if st.session_state.admin:
            with st.container(horizontal=True):
                st.space("stretch")
                if st.button("Gruppe abschließen",width=200,key="bt_gruppeD"):
                    finish_group('D')     
                st.space("stretch")
with tab2:
    raw = c.execute("""
        SELECT id, name, team_group, group_placement
        FROM teams WHERE class LIKE '%LVL1/2%'
        ORDER BY team_group ASC, group_placement ASC
        """).fetchall()
    team_list=[]
    for i in raw:
        tid, tname, tgroup, tplace = i
        if parse_to_int(tplace)<3 and not parse_to_int(tplace)==0:
            team_list.append(i)
    if len(team_list)==8:
        st.markdown("The finalists are")
        for i in team_list:
            st.markdown(i)
    else:
        st.markdown("Gruppenphase läuft noch...")
with tab3:
    semi1_team2 = "Shuttlestars"
    semi1_team1 = "Bla Bla"
    semi2_team1 = "Net Ninjas"
    semi2_team2 = "Smash Bros"

    finalist1 = "Falcons"
    finalist2 = "Smash Bros"

    champion = "Falcons"

    # =========================
    # TITLE
    # =========================
    st.markdown('<div class="bracket-title">🏆 Knockout Stage</div>', unsafe_allow_html=True)

    # =========================
    # BRACKET LAYOUT
    # =========================
    col1, col2, col3, col4, col5 = st.columns([4,1,4,1,4])

    # -------------------------
    # SEMI FINALS
    # -------------------------
    with col1:
        st.markdown("### Semi Finals")

        st.markdown(f'<div class="bracket-team">{semi1_team1}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bracket-team">{semi1_team2}</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:70px"></div>', unsafe_allow_html=True)

        st.markdown(f'<div class="bracket-team">{semi2_team1}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bracket-team">{semi2_team2}</div>', unsafe_allow_html=True)

    # -------------------------
    # CONNECTORS
    # -------------------------
    with col2:
        st.markdown('<div class="connector"></div>', unsafe_allow_html=True)
        st.markdown('<div style="height:90px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="connector"></div>', unsafe_allow_html=True)

    # -------------------------
    # FINALS
    # -------------------------
    with col3:
        st.markdown("### Finals")

        st.markdown('<div style="height:55px"></div>', unsafe_allow_html=True)

        st.markdown(f'<div class="bracket-team">{finalist1}</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:120px"></div>', unsafe_allow_html=True)

        st.markdown(f'<div class="bracket-team">{finalist2}</div>', unsafe_allow_html=True)

    # -------------------------
    # FINAL CONNECTOR
    # -------------------------
    with col4:
        st.markdown('<div class="final-connector"></div>', unsafe_allow_html=True)

    # -------------------------
    # CHAMPION
    # -------------------------
    with col5:
        st.markdown("### Winner")
        st.markdown(f'<div class="champion">🏆<br>{champion}</div>', unsafe_allow_html=True)