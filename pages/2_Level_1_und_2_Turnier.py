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
    semi1_team1 = c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','A', 1)).fetchone()
    semi1_team2 = c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','C', 1)).fetchone()
    semi2_team1 = c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','B', 1)).fetchone()
    semi2_team2 = c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','D', 1)).fetchone()

    finalist1 = "Falcons"
    finalist2 = "Smash Bros"
    winner= "---"
    winner2= "---"
    champion = "Falcons"

    # =========================
    # BRACKET LAYOUT
    # =========================
    col1, col2 = st.columns([4,2])

    # -------------------------
    # SEMI FINALS
    # -------------------------
    # with col1:
        # st.markdown("### Semi Finals")

        # st.markdown(f'<div class="bracket-team">{semi1_team1[1]}</div>', unsafe_allow_html=True)
        # st.markdown('<div style="height:30px"></div>', unsafe_allow_html=True)
        # st.markdown(f'<div class="bracket-team">{semi1_team2[1]}</div>', unsafe_allow_html=True)

        # st.markdown('<div style="height:70px"></div>', unsafe_allow_html=True)

        # st.markdown(f'<div class="bracket-team">{semi2_team1[1]}</div>', unsafe_allow_html=True)
        # st.markdown(f'<div class="bracket-team">{semi2_team2[1]}</div>', unsafe_allow_html=True)

    # -------------------------
    # CONNECTORS
    # -------------------------
    with col1:
        st.markdown(f"""
            <style>
            .scroll-container {{
                overflow-x: auto;
                overflow-y: hidden;

                width: 100%;
                padding-bottom: 10px;
            }}

            .bracket-wrapper {{
                min-width: 900px;
            }}
            .bracket-row {{
                display: flex;
                align-items: center;
                gap: 0px;
                margin-bottom: 30px;
            }}
            .team-column {{
                display: flex;
                flex-direction: column;
                gap: 40px;
            }}
            .team-column2 {{
                display: flex;
                left: 10px;
                flex-direction: column;
                gap: 182px;
            }}
            .team-column3 {{
                display: flex;
                left: 10px;
                flex-direction: column;
                gap: 182px;
            }}
            .team-box {{
                background: #262730;
                padding: 12px 20px;
                border-radius: 10px;
                width: 150px;
                text-align: center;
                font-weight: bold;
            }}
            .connector {{
                position: relative;
                width: 50px;
                height: 400px;
            }}
            .h-line {{
                position: absolute;
                left: 0;
                height: 94px;
                width: 20px;
                border-top: 4px solid #888;
                border-bottom: 4px solid #888;
                border-right: 4px solid #888;
            }}
            .h-line2 {{
                position: absolute;
                left: 0;
                height: 234px;
                width: 20px;
                border-top: 4px solid #888;
                border-bottom: 4px solid #888;
                border-right: 4px solid #888;
            }}
            .h-line.top {{
                top: 38px;
            }}
            .h-line2.top {{
                top: 82px;
            }}
            .h-line.bottom {{
                top: 268px;
            }}
            .middle-line{{
                position: absolute;
                left: 20px;
                width: 30px;
                border-top: 4px solid #888;
            }}
            .middle-line2{{
                position: absolute;
                left: 20px;
                width: 30px;
                border-top: 4px solid #888;
            }}
            .middle-line.top{{
                top: 82px;
            }}
            .middle-line2.top{{
                top: 198px;
            }}
            .middle-line.bottom{{
                top: 312px;
            }}
            </style>
            <div class="scroll-container">
                <div class="bracket-wrapper">
                    <div class="bracket-row">
                        <div class="team-column">
                            <div class="team-box">{semi1_team1[1]}</div>
                            <div class="team-box">{semi1_team2[1]}</div>
                            <div style="height:10px"></div>
                            <div class="team-box">{semi2_team1[1]}</div>
                            <div class="team-box">{semi2_team2[1]}</div>
                        </div>
                        <div class="connector">
                            <div class="h-line top"></div>
                            <div class="middle-line top"></div>
                            <div class="h-line bottom"></div>
                            <div class="middle-line bottom"></div>
                        </div>
                        <div class="team-column2">
                            <div class="team-box">
                                {winner}
                            </div>
                            <div class="team-box">
                                {winner2}
                            </div>
                        </div>
                        <div class="connector">
                            <div class="h-line2 top"></div>
                            <div class="middle-line2 top"></div>
                        </div>
                        <div class="team-column3">
                            <div class="team-box">
                                {winner}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    with st.container(horizontal=True):
        st.space("stretch")
        if st.button(":material/refresh: Reload",width=100):
            st.rerun()