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
st.set_page_config(page_title="Sommerturnier",initial_sidebar_state="expanded",layout="wide",page_icon=":badminton:")
def parse_to_int(v):
    try:
        return int(v)
    except:
        return 0
def print_table(r,group):
    h1, h2, h3, h4 = st.columns([.4,.1,.1,.1],gap="xsmall")
    h1.markdown(":blue[:material/group: **Team**]")
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
            st.markdown(":white[Turnierleitung erstellt Gruppe...]")
            st.space("stretch")
    else:
        for name, wins, losses, diff in table1:
            c1, c2, c3, c4 = st.columns([.4,.1,.1,.1],gap="xsmall")
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
        c1, c2, c3, c4 = st.columns([.4,.1,.1,.1],gap="xsmall")
        c1.space("stretch")
    return 0
def print_table_alt(r,group):
    table1=[]
    if c.execute("SELECT id FROM groups WHERE class='HD' and is_done=1 and group_name=?",(group,)).fetchone():
        col1="#CFB23F"
    else:
        col1="#FFFFFF"
    for i in r:
        if i[7]==group:
            points = i[5]-i[6]
            table1.append([i[0],i[1],i[2],f"{i[3]} : {i[4]}", f"{points}"])
    if table1==[]:
        with st.container(horizontal=True):
            st.space("stretch")
            if st.session_state.language== "german":
                st.markdown(":blue[Turnierleitung erstellt Gruppe...]")
            if st.session_state.language== "english":
                st.markdown(":blue[Group is being generated...]")
            st.space("stretch")
    else:
        rows_html = ""
        for name, wins, losses, diff, pts in table1:
            rows_html += f'''<div class="row">
                    <div class="team"><span style="color:{col1}"><font size="2">{name}</font></span></div>
                    <div class="stat"><font size="2">{wins}</font></div>
                    <div class="stat"><font size="2">{losses}</font></div>
                    <div class="stat"><font size="2">{diff}</font></div>
                    <div class="stat"><font size="2">{pts}</font></div></div>'''
            col1="#FFFFFF"
        st.markdown(f"""
            <style>
            .scroll-table {{
                overflow-x: auto;
                width: 100%;
                padding-right: 10px;
                padding-bottom: 10px;  
            }}
            .table-inner {{
                min-width: 400px;
            }}
            .row {{
                display: flex;
                align-items: center;

                padding: 10px 0;

                border-bottom: 1px solid #31333F;
            }}
            .header {{
                font-weight: bold;
                font-size: 20px;
            }}
            .team {{
                width: 300px;
                text-align: left;
            }}
            .stat {{
                width: 80px;
                text-align: center;
            }}
            </style>
            <div class="scroll-table">
                <div class="table-inner">
                    <div class="row header">
                        <div class="team" style="color:#1c83e1;"><font size="3">Team Name</font></div>
                        <div class="stat"style="color:#21c354;"><font size="3">W</font></div>
                        <div class="stat"style="color:#ff4b4b;"><font size="3">L</font></div>
                        <div class="stat" style="color:#1c83e1;"><font size="3">Sets</font></div>
                        <div class="stat" style="color:#1c83e1;"><font size="3">Pts +/-</font></div>
                    </div>
                    {rows_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
def finish_group(gname):
    groupid = c.execute("SELECT id, class FROM groups WHERE class=? and group_name=?", ('HD',gname)).fetchone()
    c.execute("UPDATE groups SET is_done=1 WHERE id=?",(groupid[0],))
    conn.commit()
    teams = c.execute("SELECT id FROM teams WHERE (class=? or class='DD') and team_group=? ORDER BY wins DESC, loses ASC, wsets DESC, lsets ASC, wpoints DESC, lpoints ASC", ('HD',gname)).fetchall()
    placement = 1
    for i in teams:
        id = i[0]
        c.execute("UPDATE teams SET group_placement=? WHERE id=?",(placement,id))
        placement+=1
    conn.commit()
    st.rerun()
def draw_tree(klasse, number_groups):
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
    loser_finals_team1 = [0,"tbd"]
    loser_finals_team2 = [0,"tbd"]
    third = [0,"tbd"]
    finals_team1 = [0,"tbd"]
    finals_team2 = [0,"tbd"]
    winner = [0,"tbd"]
    if number_groups==4:
        if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 1)).fetchone():
            quaters1_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 1)).fetchone()
        if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'D', 2)).fetchone():
            quaters1_team2 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'D', 2)).fetchone()
        if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 1)).fetchone():
            quaters2_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 1)).fetchone()
        if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 2)).fetchone():
            quaters2_team2 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 2)).fetchone()
        if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 1)).fetchone():
            quaters3_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 1)).fetchone()
        if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 2)).fetchone():
            quaters3_team2 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 2)).fetchone()
        if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'D', 1)).fetchone():
            quaters4_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'D', 1)).fetchone()
        if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 2)).fetchone():
            quaters4_team2 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 2)).fetchone()
    elif number_groups==3:
        if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and group_placement=?",(klasse, 3)).fetchone():
            S_teams = c.execute("SELECT id, name, team_group FROM teams WHERE (class=? or class='DD') and group_placement=? ORDER BY wins DESC, loses ASC, wsets DESC, lsets ASC, wpoints DESC, lpoints ASC",(klasse, 3)).fetchall()
            is_done_list = c.execute("SELECT group_name FROM groups WHERE class=? and is_done=1",(klasse,)).fetchall()
            if len(is_done_list)==3:
                if S_teams[2][2]=='C':
                    c.execute("UPDATE settings SET which_third_is_missing=3 WHERE class=?",(klasse,))
                    conn.commit()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 2)).fetchone():
                        quaters4_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 2)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 2)).fetchone():
                        quaters4_team2 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 2)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 1)).fetchone():
                        quaters1_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 1)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 1)).fetchone():
                        quaters2_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 1)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 1)).fetchone():
                        quaters3_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 1)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 2)).fetchone():
                        quaters2_team2 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 2)).fetchone()
                    if S_teams[0][2]=='A':
                        quaters1_team2 = S_teams[1]
                        quaters3_team2 = S_teams[0]
                    else:
                        quaters1_team2 = S_teams[0]
                        quaters3_team2 = S_teams[1]
                if S_teams[2][2]=='B':
                    c.execute("UPDATE settings SET which_third_is_missing=2 WHERE class=?",(klasse,))
                    conn.commit()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 2)).fetchone():
                        quaters4_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 2)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 2)).fetchone():
                        quaters4_team2 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 2)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 1)).fetchone():
                        quaters1_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 1)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 1)).fetchone():
                        quaters3_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 1)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 1)).fetchone():
                        quaters2_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 1)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 2)).fetchone():
                        quaters2_team2 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 2)).fetchone()
                    if S_teams[0][2]=='A':
                        quaters1_team2 = S_teams[1]
                        quaters3_team2 = S_teams[0]
                    else:
                        quaters1_team2 = S_teams[0]
                        quaters3_team2 = S_teams[1]
                if S_teams[2][2]=='A':
                    c.execute("UPDATE settings SET which_third_is_missing=1 WHERE class=?",(klasse,))
                    conn.commit()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 2)).fetchone():
                        quaters4_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 2)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 2)).fetchone():
                        quaters4_team2 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 2)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 1)).fetchone():
                        quaters3_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 1)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 1)).fetchone():
                        quaters1_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'B', 1)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 1)).fetchone():
                        quaters2_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'C', 1)).fetchone()
                    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 2)).fetchone():
                        quaters2_team2 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and team_group=? and group_placement=?",(klasse,'A', 2)).fetchone()
                    if S_teams[0][2]=='B':
                        quaters1_team2 = S_teams[1]
                        quaters3_team2 = S_teams[0]
                    else:
                        quaters1_team2 = S_teams[0]
                        quaters3_team2 = S_teams[1]
    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and quaters_nr_winner=1",(klasse,)).fetchone():
        semi1_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and quaters_nr_winner=1",(klasse,)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and quaters_nr_winner=2",(klasse,)).fetchone():
        semi1_team2 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and quaters_nr_winner=2",(klasse,)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and quaters_nr_winner=3",(klasse,)).fetchone():
        semi2_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and quaters_nr_winner=3",(klasse,)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and quaters_nr_winner=4",(klasse,)).fetchone():
        semi2_team2 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and quaters_nr_winner=4",(klasse,)).fetchone()


    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and semis_nr_winner=1",(klasse,)).fetchone():
        finals_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and semis_nr_winner=1",(klasse,)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and semis_nr_winner=2",(klasse,)).fetchone():
        finals_team2 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and semis_nr_winner=2",(klasse,)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and semis_nr_loser=1",(klasse,)).fetchone():
        loser_finals_team1 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and semis_nr_loser=1",(klasse,)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and semis_nr_loser=2",(klasse,)).fetchone():
        loser_finals_team2 = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and semis_nr_loser=2",(klasse,)).fetchone()
    

    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and finals_winner=1",(klasse,)).fetchone():
        winner = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and finals_winner=1",(klasse,)).fetchone()
    if c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and third_place=1",(klasse,)).fetchone():
        third = c.execute("SELECT id, name FROM teams WHERE (class=? or class='DD') and third_place=1",(klasse,)).fetchone()
    if winner[1]=="tbd":
        col1="#FFFFFF"
    else:
        col1="#CFB23F"
    with st.container():
        st.space("small")
        st.markdown(f"""
            <style>
            .scroll-container {{
                overflow-y: hidden;
                overflow-x: scroll;
                width: 100%;
                height: 100%;
                padding-right: 50px;
                min-width:400px;
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
                gap: 200px;
            }}
            .team-column3 {{
                position: relative;
                flex-direction: column;
                top:100px;
            }}
            .team-column4 {{
                position: relative;
                flex-direction: column;
                top:194px;
            }}    
            .team-box {{
                display: flex;
                justify-content: center;
                white-space: normal;
                word-break: break-word;
                font-size: 14px; 
                background: #262730;
                padding: 12px 20px;
                border-radius: 10px;
                width: 150px;
                height: 70px;
                overflow: auto;
                align-items: center;
                text-align: center;
                font-weight: bold;
                vertical-align: middle;
            }}
            .team-box.special1{{
                margin-bottom:410px;
            }}
            .team-box.special2{{
                margin-bottom:80px;
            }}
            .team-box.special3{{
                margin-bottom:40px;
            }}
            .team-box.special4{{
                margin-bottom:365px;
            }}
            .connector {{
                position: relative;
                width: 30px;
                min-width:30px;
                height:1000px;
            }}
            .h-lineq {{
                position: absolute;
                left: 0;
                height: 115px;
                width: 10px;
                border-top: 5px solid #1c83e1;
                border-bottom: 5px solid #1c83e1;
                border-right: 5px solid #1c83e1;
            }}
            .h-lineq.one {{
                top: 37px;
            }}
            .h-lineq.lose{{
                top: 858px;
            }}
            .h-lineq.two {{
                top: 307px;
            }}
            .h-lineq.three {{
                top: 579px;
            }}
            .h-lineq.four {{
                top: 847px;
            }}
            .h-lines {{
                position: absolute;
                left: 0;
                height: 274px;
                width: 10px;
                border-top: 5px solid #1c83e1;
                border-bottom: 5px solid #1c83e1;
                border-right: 5px solid #1c83e1;
            }}
            .h-lines.top {{
                top: 93px;
            }}
            .h-lines.bot {{
                top: 633px;
            }}
            .h-linef {{
                position: absolute;
                left: 0;
                height: 485px;
                width: 10px;
                border-top: 5px solid #1c83e1;
                border-bottom: 5px solid #1c83e1;
                border-right: 5px solid #1c83e1;
            }}
            .h-linef.top {{
                top: 227px;
            }}
            .middle-lineq{{
                position: absolute;
                left: 10px;
                width: 20px;
                border-top: 5px solid #1c83e1;
            }}
            .middle-lineq.one{{
                top: 93px;
            }}
            .middle-lineq.lose{{
                top: 909px;
            }}
            .middle-lineq.two{{
                top: 363px;
            }}
            .middle-lineq.three{{
                top: 633px;
            }}
            .middle-lineq.four{{
                top: 903px;
            }}
            .middle-lines{{
                position: absolute;
                left: 10px;
                width: 20px;
                border-top: 5px solid #1c83e1;
            }}
            .middle-lines.top{{
                top: 227px;
            }}
            .middle-lines.bot{{
                top: 707px;
            }}
            .middle-linef{{
                position: absolute;
                left: 10px;
                width: 20px;
                border-top: 5px solid #1c83e1;
            }}
            .middle-linef.top{{
                top: 472px;
            }}
            </style>
            <div class="scroll-container">
                <div class="bracket-wrapper">
                    <div class="bracket-row">
                        <div class="team-column">
                            <div class="team-box"><span style="color:#FFFFFF">{quaters1_team1[1]}</span></div>
                            <div class="team-box"><span style="color:#FFFFFF">{quaters1_team2[1]}</span></div>
                            <div style="height:10px"></div>
                            <div class="team-box"><span style="color:#FFFFFF">{quaters2_team1[1]}</span></div>
                            <div class="team-box"><span style="color:#FFFFFF">{quaters2_team2[1]}</span></div>
                            <div style="height:10px"></div>
                            <div class="team-box"><span style="color:#FFFFFF">{quaters3_team1[1]}</span></div>
                            <div class="team-box"><span style="color:#FFFFFF">{quaters3_team2[1]}</span></div>
                            <div style="height:10px"></div>
                            <div class="team-box"><span style="color:#FFFFFF">{quaters4_team1[1]}</span></div>
                            <div class="team-box"><span style="color:#FFFFFF">{quaters4_team2[1]}</span></div>
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
                            <div class="team-box">
                                <span style="color:#FFFFFF">{semi1_team1[1]}</span>
                            </div>
                            <div class="team-box">
                                <span style="color:#FFFFFF">{semi1_team2[1]}</span>
                            </div>
                            <div class="team-box">
                                <span style="color:#FFFFFF">{semi2_team1[1]}</span>
                            </div>
                            <div class="team-box">
                                <span style="color:#FFFFFF">{semi2_team2[1]}</span>
                            </div>
                        </div>
                        <div class="connector">
                            <div class="h-lines top"></div>
                            <div class="middle-lines top"></div>
                            <div class="h-lines bot"></div>
                            <div class="middle-lines bot"></div>
                        </div>
                        <div class="team-column3">
                            <div class="team-box special1">
                                <span style="color:#FFFFFF">{finals_team1[1]}</span>
                            </div>
                            <div class="team-box special2">
                                <span style="color:#FFFFFF">{finals_team2[1]}</span>
                            </div>
                            <div class="team-box special3">
                                <span style="color:#FFFFFF">{loser_finals_team1[1]}</span>
                            </div>
                            <div class="team-box">
                                <span style="color:#FFFFFF">{loser_finals_team2[1]}</span>
                            </div>
                        </div>
                        <div class="connector">
                            <div class="h-linef top"></div>
                            <div class="middle-linef top"></div>
                            <div class="h-lineq lose"></div>
                            <div class="middle-lineq lose"></div>
                        </div>
                        <div class="team-column4">
                            <div class="team-box special4">
                                <span style="color:{col1}">{winner[1]}</span>
                            </div>
                            <div class="team-box">
                                <span style="color:#FFFFFF">{third[1]}</span>
                            </div>
                        </div>
                        <div class="connector">
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
if "admin" not in st.session_state:
    st.session_state.admin = False
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None
if "language" not in st.session_state:
    st.session_state.language = "german"
if "input_mode" not in st.session_state:
    st.session_state.input_mode = False
#------------------
#Top Bar
#------------------
with st.container(horizontal=True):
    if st.button("🇩🇪"):
        st.session_state.language="german"
        st.rerun()
    if st.button("🇬🇧"):
        st.session_state.language="english"
        st.rerun()
    st.space("stretch")
    if st.button(":material/refresh: Reload",width=100):
        st.rerun()
if st.session_state.language== "german":
    st.subheader("Level 1-2 Turnier", anchor=False)
if st.session_state.language== "english":
    st.subheader("Level 1-2 tourney", anchor=False)
settings= c.execute("SELECT id, group_number FROM settings WHERE class =?",('HD',)).fetchall()
if st.session_state.admin and not st.session_state.input_mode:
    if st.session_state.language== "german":
        tab1,tab2,tab3=st.tabs(["Gruppenphase", "K/O-Phase","Einstellungen"])
    if st.session_state.language== "english":
        tab1,tab2,tab3=st.tabs(["Group stage", "K/O phase","Setting"])
    with tab1:
        with st.container(horizontal=True):
            st.space("stretch")
            with st.container(width=500):
                st.space("small")
                if st.session_state.language== "german":
                    grA = st.expander("Gruppe A", on_change="rerun",key="ad_gruppeA",expanded=True)
                if st.session_state.language== "english":
                    grA = st.expander("Group A", on_change="rerun",key="ad_gruppeA",expanded=True)
                with grA:
                    raw = c.execute("""
                    SELECT name, wins, loses, wsets, lsets, wpoints, lpoints, team_group
                    FROM teams WHERE class LIKE '%HD%' or class LIKE '%DD%'
                    ORDER BY wins DESC, loses ASC, wsets DESC, lsets ASC, wpoints DESC, lpoints ASC
                    """).fetchall()
                    print_table_alt(raw,'A')
                    st.space("xsmall")
                    with st.container(horizontal=True):
                        st.space("stretch")
                        if c.execute("SELECT id, class FROM groups WHERE is_done=0 and class='HD' and group_name='A'").fetchone():
                            if st.button(":red[Gruppe beenden]",width=200,key="ad_bt_gruppeA"):
                                finish_group('A')
                        else:
                            if st.button(":red[Platzierung neu eintragen]",width=200,key="ad_bt2_gruppeA"):
                                finish_group('A')
                        st.space("stretch")
                st.space("xxsmall")
                if st.session_state.language== "german":
                    grB = st.expander("Gruppe B", on_change="rerun",key="ad_gruppeB",expanded=True)
                if st.session_state.language== "english":
                    grB = st.expander("Group B", on_change="rerun",key="ad_gruppeB",expanded=True)
                with grB:
                    raw = c.execute("""
                    SELECT name, wins, loses, wsets, lsets, wpoints, lpoints, team_group
                    FROM teams WHERE class LIKE '%HD%' or class LIKE '%DD%'
                    ORDER BY wins DESC, loses ASC, wsets DESC, lsets ASC, wpoints DESC, lpoints ASC
                    """).fetchall()
                    print_table_alt(raw,'B')
                    st.space("xsmall")
                    with st.container(horizontal=True):
                        st.space("stretch")
                        if c.execute("SELECT id, class FROM groups WHERE is_done=0 and class='HD' and group_name='B'").fetchone():
                            if st.button(":red[Gruppe beenden]",width=200,key="ad_bt_gruppeB"):
                                finish_group('B')
                        else:
                            if st.button(":red[Platzierung neu eintragen]",width=200,key="ad_bt2_gruppeB"):
                                finish_group('B')  
                        st.space("stretch")
                st.space("xxsmall")
                if st.session_state.language== "german":
                    grC = st.expander("Gruppe C", on_change="rerun",key="ad_gruppeC",expanded=True)
                if st.session_state.language== "english":
                    grC = st.expander("Group C", on_change="rerun",key="ad_gruppeC",expanded=True)
                with grC:
                    raw = c.execute("""
                    SELECT name, wins, loses, wsets, lsets, wpoints, lpoints, team_group
                    FROM teams WHERE class LIKE '%HD%' or class LIKE '%DD%'
                    ORDER BY wins DESC, loses ASC, wsets DESC, lsets ASC, wpoints DESC, lpoints ASC
                    """).fetchall()
                    print_table_alt(raw,'C')
                    st.space("xsmall")
                    with st.container(horizontal=True):
                        st.space("stretch")
                        if c.execute("SELECT id, class FROM groups WHERE is_done=0 and class='HD' and group_name='C'").fetchone():
                            if st.button(":red[Gruppe beenden]",width=200,key="ad_bt_gruppeC"):
                                finish_group('C')
                        else:
                            if st.button(":red[Platzierung neu eintragen]",width=200,key="ad_bt2_gruppeC"):
                                finish_group('C')
                        st.space("stretch")
                st.space("xxsmall")
                if settings[0][1]==4:
                    if st.session_state.language== "german":
                        grD = st.expander("Gruppe D", on_change="rerun",key="ad_gruppeD",expanded=True)
                    if st.session_state.language== "english":
                        grD = st.expander("Group D", on_change="rerun",key="ad_gruppeD",expanded=True)
                    with grD:
                        raw = c.execute("""
                        SELECT name, wins, loses, wsets, lsets, wpoints, lpoints, team_group
                        FROM teams WHERE class LIKE '%HD%' or class LIKE '%DD%'
                        ORDER BY wins DESC, loses ASC, wsets DESC, lsets ASC, wpoints DESC, lpoints ASC
                        """).fetchall()
                        print_table_alt(raw,'D')
                        st.space("xsmall")
                        with st.container(horizontal=True):
                            st.space("stretch")
                            if c.execute("SELECT id, class FROM groups WHERE is_done=0 and class='HD' and group_name='D'").fetchone():
                                if st.button(":red[Gruppe beenden]",width=200,key="ad_bt_gruppeD"):
                                    finish_group('D')
                            else:
                                if st.button(":red[Platzierung neu eintragen]",width=200,key="ad_bt2_gruppeD"):
                                    finish_group('D')    
                            st.space("stretch")
            st.space("stretch")
    with tab2:
        with st.container(horizontal=True):
            draw_tree('HD',settings[0][1])
    with tab3:
        if settings[0][1]==4:
            if st.checkbox("5er Gruppen"):         
                c.execute("UPDATE settings SET group_number=3 WHERE class=?",('HD',))
                conn.commit()
                st.rerun()
        if settings[0][1]==3:
            if st.checkbox("4er Gruppen"):         
                c.execute("UPDATE settings SET group_number=4 WHERE class=?",('HD',))
                c.execute("UPDATE settings SET which_third_is_missing=0 WHERE class=?",('HD',))
                conn.commit()
                st.rerun()
else:
    if st.session_state.language== "german":
        tab1, tab2 = st.tabs(["Gruppenphase", "K/O-Phase"])
    if st.session_state.language== "english":
        tab1, tab2 = st.tabs(["Group stage", "K/O phase"])
    with tab1:
        with st.container(horizontal=True):
            st.space("stretch")
            with st.container(width=600):
                st.space("small")
                if st.session_state.language== "german":
                    grA = st.expander("Gruppe A", on_change="rerun",key="ad_gruppeA",expanded=True)
                if st.session_state.language== "english":
                    grA = st.expander("Group A", on_change="rerun",key="ad_gruppeA",expanded=True)
                with grA:
                    raw = c.execute("""
                    SELECT name, wins, loses, wsets, lsets, wpoints, lpoints, team_group
                    FROM teams WHERE class LIKE '%HD%' or class LIKE '%DD%'
                    ORDER BY wins DESC, loses ASC, wsets DESC, lsets ASC, wpoints DESC, lpoints ASC
                    """).fetchall()
                    print_table_alt(raw,'A')
                st.space("xxsmall")
                if st.session_state.language== "german":
                    grB = st.expander("Gruppe B", on_change="rerun",key="ad_gruppeB",expanded=True)
                if st.session_state.language== "english":
                    grB = st.expander("Group B", on_change="rerun",key="ad_gruppeB",expanded=True)
                with grB:
                    raw = c.execute("""
                    SELECT name, wins, loses, wsets, lsets, wpoints, lpoints, team_group
                    FROM teams WHERE class LIKE '%HD%' or class LIKE '%DD%'
                    ORDER BY wins DESC, loses ASC, wsets DESC, lsets ASC, wpoints DESC, lpoints ASC
                    """).fetchall()
                    print_table_alt(raw,'B')
                st.space("xxsmall")
                if st.session_state.language== "german":
                    grC = st.expander("Gruppe C", on_change="rerun",key="ad_gruppeC",expanded=True)
                if st.session_state.language== "english":
                    grC = st.expander("Group C", on_change="rerun",key="ad_gruppeC",expanded=True)
                with grC:
                    raw = c.execute("""
                    SELECT name, wins, loses, wsets, lsets, wpoints, lpoints, team_group
                    FROM teams WHERE class LIKE '%HD%' or class LIKE '%DD%'
                    ORDER BY wins DESC, loses ASC, wsets DESC, lsets ASC, wpoints DESC, lpoints ASC
                    """).fetchall()
                    print_table_alt(raw,'C')
                st.space("xxsmall")
                if settings[0][1]==4:
                    if st.session_state.language== "german":
                        grD = st.expander("Gruppe D", on_change="rerun",key="ad_gruppeD",expanded=True)
                    if st.session_state.language== "english":
                        grD = st.expander("Group D", on_change="rerun",key="ad_gruppeD",expanded=True)
                    with grD:
                        raw = c.execute("""
                        SELECT name, wins, loses, wsets, lsets, wpoints, lpoints, team_group
                        FROM teams WHERE class LIKE '%HD%' or class LIKE '%DD%'
                        ORDER BY wins DESC, loses ASC, wsets DESC, lsets ASC, wpoints DESC, lpoints ASC
                        """).fetchall()
                        print_table_alt(raw,'D')
            st.space("stretch")
    with tab2:
        with st.container(horizontal=True):
            draw_tree('HD',settings[0][1])