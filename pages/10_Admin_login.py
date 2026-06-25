import streamlit as st
import time
import sqlite3
from datetime import datetime
st.markdown("""
<style>
    /* Hide top header, hamburger menu, and footer */
    [data-testid="stMainMenu"] {display: none;}
    [data-testid="stToolbarActions"] {display: none;}
    [data-testid="appCreatorAvatar"] {display: none;}
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
def get_team_name(team_id):
    res = c.execute("SELECT name FROM teams WHERE id=?", (team_id,)).fetchone()
    return res[0] if res else "Unknown"
state_change = "admin123"
if "admin" not in st.session_state:
    st.session_state.admin = False
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None
if "language" not in st.session_state:
    st.session_state.language = "german"
if "input_mode" not in st.session_state:
    st.session_state.input_mode = False
if "game_class" not in st.session_state:
    st.session_state.game_class = None
if "team_class" not in st.session_state:
    st.session_state.team_class = None
if "group" not in st.session_state:
    st.session_state.group = None
if "stage" not in st.session_state:
    st.session_state.stage = None
if "team_name" not in st.session_state:
    st.session_state.team_name = None
if "searched_match" not in st.session_state:
    st.session_state.searched_match = False
if "searched_team" not in st.session_state:
    st.session_state.searched_team = False
if "searched_group" not in st.session_state:
    st.session_state.searched_group = False
if "group_class" not in st.session_state:
    st.session_state.group_class = None
with st.container(horizontal=True):
    if st.button("🇩🇪"):
        st.session_state.language="german"
        st.rerun()
    if st.button("🇬🇧"):
        st.session_state.language="english"
        st.rerun()
    st.space("stretch")
    if st.session_state.admin:
        if st.button(":material/logout: Logout",width=100):
            st.session_state.admin = False
            st.session_state.input_mode = False
            st.session_state.game_class = None
            st.session_state.stage = None
            st.session_state.searched_match = False
            st.session_state.group=None
            st.session_state.team_class=None
            st.session_state.team_name=None
            st.session_state.searched_team=False
            st.session_state.searched_group=False
            st.session_state.group_class=None
            st.rerun()
    if st.button(":material/refresh: Reload",width=100):
        st.rerun()
if st.session_state.admin:
    st.subheader(":green[Logged in]",anchor=False)
    if st.session_state.input_mode:
        if st.checkbox("Input Modus aus"):
            st.session_state.input_mode = False
            st.rerun()
    else:
        if st.checkbox("Input Modus an"):
            st.session_state.input_mode = True
            st.rerun()
    st.divider()
    st.subheader(":blue[DB Editor (Use with care)]",anchor=False)
    with st.container(horizontal=True):
        st.space("stretch")
        if st.session_state.searched_match or st.session_state.searched_team or st.session_state.searched_group:
            if st.button(":material/undo: Zurück",width=100):
                st.session_state.game_class = None
                st.session_state.stage = None
                st.session_state.searched_match = False
                st.session_state.group=None
                st.session_state.team_class=None
                st.session_state.team_name=None
                st.session_state.searched_team=False
                st.session_state.searched_group=False
                st.session_state.group_class=None
                st.rerun()
    if st.session_state.searched_match:
        klasse = st.session_state.game_class
        stage_name = st.session_state.stage
        db=None
        if [klasse, stage_name] == [None,None]:
            db=None
        elif stage_name == None:
            if c.execute("SELECT id, player1_id, player2_id, court, s1_p1, s1_p2, s2_p1, s2_p2, s3_p1, s3_p2, is_visible, match_class, stage FROM matches WHERE match_class=?",(klasse,)).fetchone():
                db = c.execute("SELECT id, player1_id, player2_id, court, s1_p1, s1_p2, s2_p1, s2_p2, s3_p1, s3_p2, is_visible, match_class, stage FROM matches WHERE match_class=?",(klasse,)).fetchall() 
        elif klasse== None:
            if c.execute("SELECT id, player1_id, player2_id, court, s1_p1, s1_p2, s2_p1, s2_p2, s3_p1, s3_p2, is_visible, match_class, stage FROM matches WHERE stage=?",(stage_name,)).fetchone():
                db = c.execute("SELECT id, player1_id, player2_id, court, s1_p1, s1_p2, s2_p1, s2_p2, s3_p1, s3_p2, is_visible, match_class, stage FROM matches WHERE stage=?",(stage_name,)).fetchall() 
        else:
            if c.execute("SELECT id, player1_id, player2_id, court, s1_p1, s1_p2, s2_p1, s2_p2, s3_p1, s3_p2, is_visible, match_class, stage FROM matches WHERE match_class=? and stage=?",(klasse,stage_name)).fetchall():
                db = c.execute("SELECT id, court, player1_id, player2_id, s1_p1, s1_p2, s2_p1, s2_p2, s3_p1, s3_p2, is_visible, match_class, stage FROM matches WHERE match_class=? and stage=?",(klasse,stage_name)).fetchall()
        if db==None:
            with st.container(horizontal=True):
                st.space("stretch")
                st.error("Kein Match gefunden.",width=220,icon=":material/chat_error:")
                st.space("stretch")
        else:
            st.markdown(f"{len(db)} matching matches found.")
            for match in db:
                    mid, court, p1,p2,s1_p1, s1_p2, s2_p1, s2_p2, s3_p1, s3_p2, is_visible, match_class, stage = match
                    with st.form(f"match_edit_{mid}"):
                        with st.container(horizontal=True,border=False,key=f"cont_{mid}"):
                            st.space("xsmall")
                            st.markdown(f"{get_team_name(p1)} vs. {get_team_name(p2)}")
                            st.space("xxlarge")
                            new_mid = st.text_input("ID",width=60,value=str(mid) if mid is not None else "",key=f"mid_{mid}")
                            new_court = st.text_input("Court",width=60,value=str(court) if court is not None else "",key=f"court_{mid}")
                            new_s1_p1 = st.text_input("s1_p1",width=60,value=str(s1_p1) if s1_p1 is not None else "",key=f"s1p1_{mid}")
                            new_s1_p2 = st.text_input("s1_p2",width=60,value=str(s1_p2) if s1_p2 is not None else "",key=f"s1p2_{mid}")
                            new_s2_p1 = st.text_input("s2_p1",width=60,value=str(s2_p1) if s2_p1 is not None else "",key=f"s2p1_{mid}")
                            new_s2_p2 = st.text_input("s2_p2",width=60,value=str(s2_p2) if s2_p2 is not None else "",key=f"s2p2_{mid}")
                            new_s3_p1 = st.text_input("s3_p1",width=60,value=str(s3_p1) if s3_p1 is not None else "",key=f"s3p1_{mid}")
                            new_s3_p2 = st.text_input("s3_p2",width=60,value=str(s3_p2) if s3_p2 is not None else "",key=f"s3p2_{mid}")
                            new_visible = st.text_input("Visible",width=60,value=str(is_visible) if is_visible is not None else "",key=f"vis_{mid}")
                            new_class = st.text_input("Class",width=80,value=str(match_class) if match_class is not None else "",key=f"class_{mid}")
                            new_stage = st.text_input("Stage",width=80,value=str(stage) if stage is not None else "",key=f"stage_{mid}")
                            st.space("stretch")
                            submit = st.form_submit_button(":material/update:\u00A0\u00A0Update",width=100)
                    if submit:
                        if not new_mid == mid:
                            c.execute("UPDATE matches SET id=? WHERE id=?", (new_mid,mid))
                        if not new_court == court:
                            c.execute("UPDATE matches SET court=? WHERE id=?", (new_court,new_mid))
                        if not new_s1_p1 == s1_p1:
                            c.execute("UPDATE matches SET s1_p1=? WHERE id=?", (new_s1_p1,new_mid))
                        if not new_s1_p2 == s1_p2:
                            c.execute("UPDATE matches SET s1_p2=? WHERE id=?", (new_s1_p2,new_mid))
                        if not new_s2_p1 == s2_p1:
                            c.execute("UPDATE matches SET s2_p1=? WHERE id=?", (new_s2_p1,new_mid))
                        if not new_s2_p2 == s2_p2:
                            c.execute("UPDATE matches SET s2_p2=? WHERE id=?", (new_s2_p2,new_mid))
                        if not new_s3_p1 == s3_p1 or not (s3_p1==None and new_s3_p1==""):
                            if new_s3_p1 == "":
                                new_s3_p1=None
                            c.execute("UPDATE matches SET s3_p1=? WHERE id=?", (new_s3_p1,new_mid))
                        if not new_s3_p2 == s3_p2 or not (s3_p2==None and new_s3_p2==""):
                            if new_s3_p2 == "":
                                new_s3_p2=None
                            c.execute("UPDATE matches SET s3_p2=? WHERE id=?", (new_s3_p2,new_mid))
                        if not new_visible == court:
                            c.execute("UPDATE matches SET is_visible=? WHERE id=?", (new_visible,new_mid))
                        if not new_class == court:
                            c.execute("UPDATE matches SET match_class=? WHERE id=?", (new_class,new_mid))
                        if not new_stage == court:
                            c.execute("UPDATE matches SET stage=? WHERE id=?", (new_stage,new_mid))
                        conn.commit()
                        st.session_state.game_class = None
                        st.session_state.stage = None
                        st.session_state.searched_match=False
                        st.rerun()               
    elif st.session_state.searched_team:
        klasse = st.session_state.team_class
        gruppe = st.session_state.group
        name = st.session_state.team_name
        teams= None
        if [klasse, gruppe, name] == [None,None,None]:
            with st.container(horizontal=True):
                teams=None
        elif name == None:
            if gruppe == None:
                if c.execute("SELECT * FROM teams WHERE class=?", (klasse,)).fetchone():
                    teams = c.execute("SELECT * FROM teams WHERE class=?", (klasse,)).fetchall()
            elif klasse== None:
                if c.execute("SELECT * FROM teams WHERE team_group=?", (gruppe,)).fetchone():
                    teams = c.execute("SELECT * FROM teams WHERE team_group=?", (gruppe,)).fetchall()
            else:
                if c.execute("SELECT * FROM teams WHERE class=? and team_group=?", (klasse, gruppe)).fetchone():
                    teams = c.execute("SELECT * FROM teams WHERE class=? and team_group=?", (klasse, gruppe)).fetchall()
        else:
            if gruppe == None and klasse == None:
                if c.execute("SELECT * FROM teams WHERE name LIKE ?", ('%'+name+'%',)).fetchone():
                    teams = c.execute("SELECT * FROM teams WHERE name LIKE ?", ('%'+name+'%',)).fetchall()
            elif gruppe==None:
                if c.execute("SELECT * FROM teams WHERE class=? and name LIKE ? ", (klasse,'%'+name+'%')).fetchone():
                    teams = c.execute("SELECT * FROM teams WHERE class=? and name LIKE ?", (klasse,'%'+name+'%')).fetchall()
            elif klasse== None:
                if c.execute("SELECT * FROM teams WHERE team_group=? and name LIKE ?", (gruppe,'%'+name+'%')).fetchone():
                    teams = c.execute("SELECT * FROM teams WHERE team_group=? and name LIKE ?", (gruppe,'%'+name+'%')).fetchall()
            else:
                if c.execute("SELECT * FROM teams WHERE class=? and team_group=? and name LIKE ?", (klasse, gruppe,'%'+name+'%')).fetchone():
                    teams = c.execute("SELECT * FROM teams WHERE class=? and team_group=? and name LIKE ?", (klasse, gruppe,'%'+name+'%')).fetchall()
        if teams== None:
            with st.container(horizontal=True):
                st.space("stretch")
                st.error("Kein Team gefunden.",width=220,icon=":material/chat_error:")
                st.space("stretch")
        else:
            st.markdown(f"{len(teams)} matching teams found.")
            for t in teams:
                tid, name, wins,loses,wsets,lsets,wpoints,lpoints,total_wins,total_loses,total_wsets,total_lsets,total_wpoints,total_lpoints,team_class,team_group,group_placement,quaters_nr_winner,semis_nr_winner,third_place,semis_nr_loser,finals_winner = t
                with st.form(f"team_edit_{tid}"):
                    with st.container(horizontal=True,border=False,key=f"cont1_{tid}"):
                        new_tid = st.text_input("ID",width=60,value=str(tid) if tid is not None else "",key=f"tid_{tid}")
                        new_name = st.text_input("Name",width=200,value=str(name) if name is not None else "",key=f"court_{tid}")
                        new_group = st.text_input("Group",width=60,value=str(team_group) if team_group is not None else "",key=f"team_group_{tid}")
                        new_class = st.text_input("Class",width=80,value=str(team_class) if team_class is not None else "",key=f"team_class_{tid}")
                        new_placement = st.text_input("GPlace",width=80,value=str(group_placement) if group_placement is not None else "",key=f"group_placement_{tid}")
                    with st.container(horizontal=True,border=False,key=f"cont2_{tid}"):
                        new_wins = st.text_input("Wins",width=60,value=str(wins) if wins is not None else "",key=f"wins_{tid}")
                        new_loses = st.text_input("Loses",width=60,value=str(loses) if loses is not None else "",key=f"loses_{tid}")
                        new_wsets = st.text_input("Wsets",width=60,value=str(wsets) if wsets is not None else "",key=f"wsets_{tid}")
                        new_lsets = st.text_input("Lsets",width=60,value=str(lsets) if lsets is not None else "",key=f"lsets_{tid}")
                        new_wpoints = st.text_input("Wpts",width=60,value=str(wpoints) if wpoints is not None else "",key=f"wpoints_{tid}")
                        new_lpoints = st.text_input("Lpts",width=60,value=str(lpoints) if lpoints is not None else "",key=f"lpoints_{tid}")
                        new_twins = st.text_input("TWins",width=60,value=str(total_wins) if total_wins is not None else "",key=f"total_wins_{tid}")
                        new_tloses = st.text_input("TLoses",width=60,value=str(total_loses) if total_loses is not None else "",key=f"total_loses_{tid}")
                        new_twsets = st.text_input("TWsets",width=60,value=str(total_wsets) if total_wsets is not None else "",key=f"total_wsets_{tid}")
                        new_tlsets = st.text_input("TLsets",width=60,value=str(total_lsets) if total_lsets is not None else "",key=f"total_lsets_{tid}")
                        new_twpoints = st.text_input("TWpts",width=60,value=str(total_wpoints) if total_wpoints is not None else "",key=f"total_wpoints_{tid}")
                        new_tlpoints = st.text_input("TLpts",width=60,value=str(total_lpoints) if total_lpoints is not None else "",key=f"total_lpoints_{tid}")
                        st.space("stretch")
                        submit = st.form_submit_button(":material/update:\u00A0\u00A0Update",width=100)
                if submit:
                    if not new_tid == tid:
                        c.execute("UPDATE teams SET id=? WHERE id=?", (new_tid,tid))
                    if not new_name == name:
                        c.execute("UPDATE teams SET name=? WHERE id=?", (new_name,new_tid))
                    if not new_group == team_group:
                        c.execute("UPDATE teams SET team_group=? WHERE id=?", (new_group,new_tid))
                    if not new_class == team_class:
                        c.execute("UPDATE teams SET class=? WHERE id=?", (new_class,new_tid))
                    if not new_placement == group_placement:
                        c.execute("UPDATE teams SET group_placement=? WHERE id=?", (new_placement,new_tid))
                    if not new_wins == wins:
                        c.execute("UPDATE teams SET wins=? WHERE id=?", (new_wins,new_tid))
                    if not new_loses == loses:
                        c.execute("UPDATE teams SET loses=? WHERE id=?", (new_loses,new_tid))
                    if not new_wsets == wsets:
                        c.execute("UPDATE teams SET wsets=? WHERE id=?", (new_wsets,new_tid))
                    if not new_lsets == lsets:
                        c.execute("UPDATE teams SET lsets=? WHERE id=?", (new_lsets,new_tid))
                    if not new_wpoints == wpoints:
                        c.execute("UPDATE teams SET wpoints=? WHERE id=?", (new_wpoints,new_tid))
                    if not new_lpoints == lpoints:
                        c.execute("UPDATE teams SET lpoints=? WHERE id=?", (new_lpoints,new_tid))
                    if not new_twins == total_wins:
                        c.execute("UPDATE teams SET total_wins=? WHERE id=?", (new_twins,new_tid))
                    if not new_tloses == total_loses:
                        c.execute("UPDATE teams SET total_loses=? WHERE id=?", (new_tloses,new_tid))
                    if not new_twsets == total_wsets:
                        c.execute("UPDATE teams SET total_wsets=? WHERE id=?", (new_twsets,new_tid))
                    if not new_tlsets == total_lsets:
                        c.execute("UPDATE teams SET total_lsets=? WHERE id=?", (new_tlsets,new_tid))
                    if not new_twpoints == total_wpoints:
                        c.execute("UPDATE teams SET total_wpoints=? WHERE id=?", (new_twpoints,new_tid))
                    if not new_tlpoints == total_lpoints:
                        c.execute("UPDATE teams SET total_lpoints=? WHERE id=?", (new_tlpoints,new_tid))
                    conn.commit()
                    st.session_state.group=None
                    st.session_state.team_class=None
                    st.session_state.team_name=None
                    st.session_state.searched_team=None
                    st.rerun()
    elif st.session_state.searched_group:
        klasse = st.session_state.group_class
        groups = None
        if klasse == None:
            groups = None
        else:
            if c.execute("SELECT * FROM groups WHERE class=?", (klasse,)).fetchone():
                groups = c.execute("SELECT * FROM groups WHERE class=?", (klasse,)).fetchall()
        if groups == None:
            with st.container(horizontal=True):
                st.space("stretch")
                st.error("Keine Gruppe gefunden.",width=220,icon=":material/chat_error:")
                st.space("stretch")
        else:
            for g in groups:
                gid, group_class, group_name, is_done = g
                with st.form(f"group_edit_{gid}"):
                    with st.container(horizontal=True,border=False,key=f"cont1_{gid}"):
                        new_gid = st.text_input("ID",width=60,value=str(gid) if gid is not None else "",key=f"gid_{gid}")
                        new_name = st.text_input("Name",width=200,value=str(group_name) if group_name is not None else "",key=f"gname_{gid}")
                        new_done = st.text_input("is_done",width=60,value=str(is_done) if is_done is not None else "",key=f"done_{gid}")
                        new_class = st.text_input("Klasse",width=80,value=str(group_class) if group_class is not None else "",key=f"group_class_{gid}")
                        st.space("stretch")
                        submit = st.form_submit_button(":material/update:\u00A0\u00A0Update",width=100)
                    if submit:
                        if not new_gid == gid:
                            c.execute("UPDATE groups SET id=? WHERE id=?", (new_gid,gid))
                        if not new_name == group_name:
                            c.execute("UPDATE teams SET group_name=? WHERE id=?", (new_name,new_gid))
                        if not new_done == is_done:
                            c.execute("UPDATE teams SET is_done=? WHERE id=?", (new_done,new_gid))
                        if not new_class == group_class:
                            c.execute("UPDATE teams SET class=? WHERE id=?", (new_class,new_gid))
                        conn.commit()
                        st.session_state.group_class=None
                        st.session_state.searched_group=None
                        st.rerun()
    else:
        ms = st.expander("Match search",expanded=False, key = "ms_key")
        with ms:
            with st.form("search_match", clear_on_submit=True,border=False):
                with st.container(horizontal=True):
                    klasse = st.selectbox("Klasse", ['LVL1/2','MX','DD','HD'],width=150, label_visibility="collapsed", placeholder="Klasse", index=None)
                    stage_name = st.selectbox("Stage", ["Bracket","Quaters", "Semis", "Final", "Loser Final"], width=150,label_visibility="collapsed",placeholder="Stage", index=None)
                    st.space("stretch")
                    submit = st.form_submit_button(":material/Search:\u00A0\u00A0Suchen",width=100)
            if submit:
                if klasse in ["LVL1/2","MX","DD","HD"]:
                    st.session_state.game_class = klasse
                if stage_name in ["Bracket","Quaters", "Semis", "Final", "Loser Final"]:
                    st.session_state.stage = stage_name
                st.session_state.searched_match=True
                st.rerun()
        ts = st.expander("Team search",expanded=False, key = "ts_key")
        with ts:
            with st.form("search_team", clear_on_submit=True,border=False):
                with st.container(horizontal=True):
                    klasse = st.selectbox("Klasse", ['LVL1/2','MX','DD','HD'],width=150, label_visibility="collapsed", placeholder="Klasse", index=None)
                    gruppe = st.selectbox("Gruppe", ["A","B","C","D"],width=100, label_visibility="collapsed", placeholder="Gruppe", index=None)
                    team_name = st.text_input("Name", width=150,label_visibility="collapsed",placeholder="Name")
                    if team_name=='':
                        team_name=None
                    st.space("stretch")
                    submit = st.form_submit_button(":material/Search:\u00A0\u00A0Suchen",width=100)
            if submit:
                if klasse in ["LVL1/2", "MX", "DD", "HD"]:
                    st.session_state.team_class = klasse
                if gruppe in ["A", "B", "C", "D"]:
                    st.session_state.group = gruppe
                if not team_name == None:
                    st.session_state.team_name = team_name
                st.session_state.searched_team=True
                st.rerun()
        gs = st.expander("Group search",expanded=False, key = "gs_key")
        with gs:
            with st.form("search_group", clear_on_submit=True,border=False):
                with st.container(horizontal=True):
                    klasse = st.selectbox("Klasse", ['LVL1/2','MX','DD','HD'],width=150, label_visibility="collapsed", placeholder="Klasse", index=None)
                    st.space("stretch")
                    submit = st.form_submit_button(":material/Search:\u00A0\u00A0Suchen",width=100)
                if submit:
                    if klasse in ["LVL1/2", "MX", "DD", "HD"]:
                        st.session_state.group_class = klasse
                    st.session_state.searched_group=True
                    st.rerun()
        
else:
    st.subheader("Admin Login",anchor=False)
    input = st.text_input("Password", type="password",label_visibility="collapsed",width=300)
    if st.button(":material/login: Login",width=100):
        if input == state_change:
            st.session_state.admin = True
            st.rerun()
        else:
            st.error("Wrong password")