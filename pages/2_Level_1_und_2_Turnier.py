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
def fill_in_tbd(candidates):
    modified=[]
    for n in candidates:
        if n == None:
            a=[-1,"tbd"]
            modified.append(a)
        else:
            modified.append(n)
        


if "admin" not in st.session_state:
    st.session_state.admin = False
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None
if "stt" not in st.session_state:
    st.session_state.stt = False
if "language" not in st.session_state:
    st.session_state.language = "german"
st.subheader("Level 1-2 Turnier", anchor=False)
tab1, tab2 = st.tabs(["Gruppenphase", "K/O-Phase"])
with tab1:
    with st.container():
        st.space("small")
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
        st.space("xxsmall")
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
        st.space("xxsmall")
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
        st.space("xxsmall")
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
    quaters1_team1 = [0,"tbd"]
    quaters1_team2 = [0,"tbd"]
    quaters2_team1 = [0,"tbd"]
    quaters2_team2 = [0,"tbd"]
    quaters3_team1 = [0,"tbd"]
    quaters3_team2 = [0,"tbd"]
    quaters4_team1 = [0,"tbd"]
    quaters4_team2 = [0,"tbd"]
    semi1_team1 = [0,"tbd"]
    semi1_team2 = [0,"tbd"]
    semi2_team1 = [0,"tbd"]
    semi2_team2 = [0,"tbd"]
    finals_team1 = [0,"tbd"]
    finals_team2 = [0,"tbd"]
    winner = [0,"tbd"]
    if c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','A', 1)).fetchone():
        quaters1_team1 = c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','A', 1)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','D', 2)).fetchone():
        quaters1_team2 = c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','D', 2)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','C', 1)).fetchone():
        quaters2_team1 = c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','C', 1)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','B', 2)).fetchone():
        quaters2_team2 = c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','B', 2)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','B', 1)).fetchone():
        quaters3_team1 = c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','B', 1)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','C', 2)).fetchone():
        quaters3_team2 = c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','C', 2)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','D', 1)).fetchone():
        quaters4_team1 = c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','D', 1)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','A', 2)).fetchone():
        quaters4_team2 = c.execute("SELECT id, name FROM teams WHERE class=? and team_group=? and group_placement=?",('LVL1/2','A', 2)).fetchone()

    if c.execute("SELECT id, name FROM teams WHERE class=? and quaters_nr_winner=1",('LVL1/2',)).fetchone():
        semi1_team1 = c.execute("SELECT id, name FROM teams WHERE class=? and quaters_nr_winner=1",('LVL1/2',)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE class=? and quaters_nr_winner=2",('LVL1/2',)).fetchone():
        semi1_team2 = c.execute("SELECT id, name FROM teams WHERE class=? and quaters_nr_winner=2",('LVL1/2',)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE class=? and quaters_nr_winner=3",('LVL1/2',)).fetchone():
        semi2_team1 = c.execute("SELECT id, name FROM teams WHERE class=? and quaters_nr_winner=3",('LVL1/2',)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE class=? and quaters_nr_winner=4",('LVL1/2',)).fetchone():
        semi2_team2 = c.execute("SELECT id, name FROM teams WHERE class=? and quaters_nr_winner=4",('LVL1/2',)).fetchone()


    if c.execute("SELECT id, name FROM teams WHERE class=? and semis_nr_winner=1",('LVL1/2',)).fetchone():
        finals_team1 = c.execute("SELECT id, name FROM teams WHERE class=? and semis_nr_winner=1",('LVL1/2',)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE class=? and semis_nr_winner=2",('LVL1/2',)).fetchone():
        finals_team2 = c.execute("SELECT id, name FROM teams WHERE class=? and semis_nr_winner=2",('LVL1/2',)).fetchone()
    

    if c.execute("SELECT id, name FROM teams WHERE class=? and finals_winner=1",('LVL1/2',)).fetchone():
        winner = c.execute("SELECT id, name FROM teams WHERE class=? and finals_winner=1",('LVL1/2',)).fetchone()
    with st.container():
        st.space("small")
        col1, col2 = st.columns([4,2])
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
                    min-width: 400px;
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
                    flex-direction: column;
                    gap: 180px;
                }}
                .team-column3 {{
                    display: flex;
                    flex-direction: column;
                    gap: 406px;
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
                    height:780px;
                }}
                .h-lineq {{
                    position: absolute;
                    left: 0;
                    height: 94px;
                    width: 20px;
                    border-top: 4px solid #888;
                    border-bottom: 4px solid #888;
                    border-right: 4px solid #888;
                }}
                .h-lineq.one {{
                    top: 0px;
                }}
                .h-lineq.two {{
                    top: 228px;
                }}
                .h-lineq.three {{
                    top: 458px;
                }}
                .h-lineq.four {{
                    top: 688px;
                }}
                .h-lines {{
                    position: absolute;
                    left: 0;
                    height: 234px;
                    width: 20px;
                    border-top: 4px solid #888;
                    border-bottom: 4px solid #888;
                    border-right: 4px solid #888;
                }}
                .h-lines.top {{
                    top: 44px;
                }}
                .h-lines.bot {{
                    top: 504px;
                }}
                .h-linef {{
                    position: absolute;
                    left: 0;
                    height: 460px;
                    width: 20px;
                    border-top: 4px solid #888;
                    border-bottom: 4px solid #888;
                    border-right: 4px solid #888;
                }}
                .h-linef.top {{
                    top: 160px;
                }}
                .middle-lineq{{
                    position: absolute;
                    left: 20px;
                    width: 30px;
                    border-top: 4px solid #888;
                }}
                .middle-lineq.one{{
                    top: 44px;
                }}
                .middle-lineq.two{{
                    top: 274px;
                }}
                .middle-lineq.three{{
                    top: 504px;
                }}
                .middle-lineq.four{{
                    top: 734px;
                }}
                .middle-lines{{
                    position: absolute;
                    left: 20px;
                    width: 30px;
                    border-top: 4px solid #888;
                }}
                .middle-lines.top{{
                    top: 160px;
                }}
                .middle-lines.bot{{
                    top: 616px;
                }}
                .middle-linef{{
                    position: absolute;
                    left: 20px;
                    width: 30px;
                    border-top: 4px solid #888;
                }}
                .middle-linef.top{{
                    top: 388px;
                }}
                </style>
                <div class="scroll-container">
                    <div class="bracket-wrapper">
                        <div class="bracket-row">
                            <div class="team-column">
                                <div class="team-box">{quaters1_team1[1]}</div>
                                <div class="team-box">{quaters1_team2[1]}</div>
                                <div style="height:10px"></div>
                                <div class="team-box">{quaters2_team1[1]}</div>
                                <div class="team-box">{quaters2_team2[1]}</div>
                                <div style="height:10px"></div>
                                <div class="team-box">{quaters3_team1[1]}</div>
                                <div class="team-box">{quaters3_team2[1]}</div>
                                <div style="height:10px"></div>
                                <div class="team-box">{quaters4_team1[1]}</div>
                                <div class="team-box">{quaters4_team2[1]}</div>
                            </div>
                            <div class="connector">
                                <div class="h-lineq one"></div>
                                <div class="middle-lineq one"></div>
                                <div class="h-lineq two"></div>
                                <div class="middle-lineq two"></div>
                                <div class="h-lineq three"></div>
                                <div class="middle-lineq three"></div>
                                <div class="h-lineq four"></div>
                                <div class="middle-lineq four"></div>
                            </div>
                            <div class="team-column2">
                                <div class="team-box top">
                                    {semi1_team1[1]}
                                </div>
                                <div class="team-box">
                                    {semi1_team2[1]}
                                </div>
                                <div class="team-box">
                                    {semi2_team1[1]}
                                </div>
                                <div class="team-box">
                                    {semi2_team2[1]}
                                </div>
                            </div>
                            <div class="connector">
                                <div class="h-lines top"></div>
                                <div class="middle-lines top"></div>
                                <div class="h-lines bot"></div>
                                <div class="middle-lines bot"></div>
                            </div>
                            <div class="team-column3">
                                <div class="team-box">
                                    {finals_team1[1]}
                                </div>
                                <div class="team-box">
                                    {finals_team2[1]}
                                </div>
                            </div>
                            <div class="connector">
                                <div class="h-linef top"></div>
                                <div class="middle-linef top"></div>
                            </div>
                            <div class="team-column4">
                                <div class="team-box">
                                    {winner[1]}
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