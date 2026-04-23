import streamlit as st
import sqlite3
from datetime import datetime
import time
st.markdown("""
<style>
    /* Hide top header, hamburger menu, and footer */
    [data-testid="stMainMenu"] {display: none;}
    [data-testid="stToolbarActions"] {display: none;}
    [data-testid="appCreatorAvatar"] {display: none;}
</style>
""", unsafe_allow_html=True)
# --- DATABASE SETUP ---
class Player:
    def __init__(self,a,b=0,c=0,d=0,e=0):
       self.name=a 
       self.wins=b
       self.loses=c
       self.wpoints=d
       self.lpoints=e
conn = sqlite3.connect("tournament.db", check_same_thread=False)
c = conn.cursor()
stats = sqlite3.connect("stats.db",check_same_thread=False)
s =stats.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player1 INTEGER,
    player2 INTEGER,
    court INTEGER,
    s1_p1 INTEGER,
    s1_p2 INTEGER,
    s2_p1 INTEGER,
    s2_p2 INTEGER,
    s3_p1 INTEGER,
    s3_p2 INTEGER,
    last_updated TIMESTAMP,
    is_new INTEGER DEFAULT 0
)
""")
conn.commit()
s.execute("""
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    wins INTEGER,
    loses INTEGER,
    wpoints INTEGER,
    lpoints INTEGER
)
""")
stats.commit()
st.set_page_config(initial_sidebar_state="expanded")
# --- SESSION STATE ---
if "admin" not in st.session_state:
    st.session_state.admin = False

if "selected_match" not in st.session_state:
    st.session_state.selected_match = None

if "new_updates" not in st.session_state:
    st.session_state.new_updates = False

if "team_view" not in st.session_state:
    st.session_state.team_view = None

st.title("Sommerturnier",anchor=False)

# --- HELPER ---
def parse_score(value):
    try:
        return int(value)
    except:
        return 0
def fetch_initials(str1, str2):
    try:
        if not str1[0]==str2[0]:
            return [str1[0],str2[0]]
        else:
            a=[str1[0],str1[1]]
            b=[str2[0],str2[1]]
            return [''.join(a),''.join(b)]
    except:
        return str
    
def view_matches(value):
    # --- FETCH MATCHES ---
    matches = c.execute("""
    SELECT id, player1, player2, court,
        s1_p1, s1_p2,
        s2_p1, s2_p2,
        s3_p1, s3_p2,
        last_updated, is_new
    FROM matches
    """).fetchall()
    if st.session_state.selected_match is None:
        with st.container(horizontal=True):
            st.space("xxsmall")
            st.subheader("On-going matches:", anchor=False)
            st.space("stretch")
            if st.button("↻ Refresh"):
                st.rerun()  
        if c.fetchone!=None:
            for match in matches:
                match_id, p1, p2, crt, *rest = match
                is_new = rest[-1]
                title = f"Court {crt}:\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0***{p1}*** vs ***{p2}***"
                if is_new and st.session_state.admin:
                    title += " ‼️"
                if st.session_state.admin:
                    with st.container(horizontal=True):                   
                        if st.button(title, key=f"open_{match_id}",width=500):
                            st.session_state.selected_match = match_id
                            st.rerun()
                        st.space("stretch")
                        if st.session_state.admin:
                            if st.button("🗑️",key=f"del_{match_id}",width=50):
                                c.execute("DELETE FROM matches WHERE id=?", (match_id,))
                                conn.commit()
                                st.session_state.selected_match = None
                                st.rerun()
                else:
                    with st.container(horizontal=True):
                        st.space("stretch")
                        if st.button(title, key=f"open_{match_id}",width=500):
                            st.session_state.selected_match = match_id 
                            st.rerun()      
                        st.space("stretch")                             
        
    else:
        match_id = st.session_state.selected_match
        match = c.execute("""
        SELECT id, player1, player2, court,
            s1_p1, s1_p2,
            s2_p1, s2_p2,
            s3_p1, s3_p2,
            last_updated, is_new
        FROM matches WHERE id=?
        """, (match_id,)).fetchone()
        (match_id, p1, p2, crt,
        s1p1, s1p2,
        s2p1, s2p2,
        s3p1, s3p2,
        last_updated, is_new) = match
        with st.container(horizontal=True):
            st.space("xxsmall")
            st.subheader(f"***{p1}*** vs ***{p2}***",anchor=False,width="content",text_alignment="left")
            st.space("stretch")
            if st.button("⬅ Back"):
                st.session_state.selected_match = None
                st.rerun()
            if st.button("↻ Refresh"):
                st.rerun()        
        if is_new and st.session_state.admin:
            c.execute("UPDATE matches SET is_new=0 WHERE id=?", (match_id,))
            conn.commit()
            st.session_state.new_updates = False
        # --- INPUT FORM ---
        with st.form('submit_results'):
            shorts=fetch_initials(p1,p2)
            shp1=shorts[0]
            shp2=shorts[1]
            c1,c2,c3=st.columns(3,border=False)
            point_cell_width=45
            with c1:
                st.markdown("**Set 1**",text_alignment="center")
                with st.container(horizontal=True,vertical_alignment="center",height=100):
                    set1_p1 = parse_score(st.text_input(
                        f"{shp1}",
                        value=str(s1p1) if s1p1 else "",
                        key="s1p1", width=point_cell_width, label_visibility="collapsed"
                    ))
                    st.space("stretch")
                    st.markdown(":",text_alignment="center")
                    st.space("stretch")
                    set1_p2 = parse_score(st.text_input(
                        f"{shp2}",
                        value=str(s1p2) if s1p2 else "",
                        key="s1p2", width=point_cell_width, label_visibility="collapsed"
                    ))
            with c2:
                st.markdown("**Set 2**",text_alignment="center")
                with st.container(horizontal=True,vertical_alignment="center",height=100):
                    set2_p1 = parse_score(st.text_input(
                        f"{shp1}",
                        value=str(s2p1) if s2p1 else "",
                        key="s2p13", width=point_cell_width, label_visibility="collapsed"
                    ))
                    st.space("stretch")
                    st.markdown(":",text_alignment="center")
                    st.space("stretch")
                    set2_p2 = parse_score(st.text_input(
                        f"{shp2}",
                        value=str(s2p2) if s2p2 else "",
                        key="s2p2", width=point_cell_width, label_visibility="collapsed"
                    ))
            with c3:
                st.markdown("**Set 3 (optional)**",text_alignment="center")
                with st.container(horizontal=True,vertical_alignment="center",height=100):
                    set3_p1_raw = st.text_input(
                        f"{shp1}",
                        value=str(s3p1) if s3p1 else "",
                        key="s3p1", width=point_cell_width, label_visibility="collapsed"
                    )
                    set3_p1 = parse_score(set3_p1_raw)
                    st.space("stretch")
                    st.markdown(":",text_alignment="center")
                    st.space("stretch")
                    set3_p2_raw = st.text_input(
                        f"{shp2}",
                        value=str(s3p2) if s3p2 else "",
                        key="s3p2", width=point_cell_width, label_visibility="collapsed"
                    )
                    set3_p2 = parse_score(set3_p2_raw)
            with st.container(horizontal=True):
                st.space("stretch")
                res=st.form_submit_button("Submit Results")
                st.space("stretch")
            if res:
                if set3_p1_raw == "" and set3_p2_raw == "":
                    s3p1_val = None
                    s3p2_val = None
                else:
                    s3p1_val = set3_p1
                    s3p2_val = set3_p2
                
                c.execute("""
                    UPDATE matches 
                    SET s1_p1=?, s1_p2=?,
                        s2_p1=?, s2_p2=?,
                        s3_p1=?, s3_p2=?,
                        last_updated=?,
                        is_new=1
                    WHERE id=?
                """, (
                    set1_p1, set1_p2,
                    set2_p1, set2_p2,
                    s3p1_val, s3p2_val,
                    datetime.now(),
                    match_id
                ))
                conn.commit()
                st.session_state.new_updates = True
                st.success("Result submitted")
    return None
adminlogin=st.Page("./pages/10_Admin_login.py", title="Login", icon=":material/login:")
matchview=st.Page(view_matches(1), title="Match Overview")
teamview=st.Page("./pages/1_Result_overview.py",title="Team Overview")

# --- SIDEBAR ---
#with st.sidebar:
    

# --- ADMIN PANEL ---
if st.session_state.admin and not st.session_state.selected_match:
    st.subheader("➕ Add Team", anchor=False)
    with st.form('add_team_form',clear_on_submit=True):
        with st.container(horizontal=True):
            n = st.text_input("Team Name",placeholder="Team Name", width=200, label_visibility="collapsed")
            st.space("stretch")
            submit=st.form_submit_button("Add Team")
            if submit:
                s.execute("""
                    INSERT INTO teams
                    (name, wins, loses, wpoints, lpoints)
                    VALUES (?, 0, 0, 0, 0)
                """,(n,))
                stats.commit()
                st.success("Match added")
                st.rerun()    
    st.subheader("➕ Add Match", anchor=False)
    teams = s.execute("""
        SELECT id, name, wins, loses, wpoints, lpoints
        FROM teams
    """).fetchall()
    drop_down_choices=[]
    if s.fetchone!=None:
        drop_down_choices=[team[1] for team in teams]
    with st.form('add_match_form',clear_on_submit=True):
         
        col1, col2, col3, col4 = st.columns([2,2,1,1])
        with col1:
            p1 = st.selectbox("Team 1",placeholder="Team 1",options = drop_down_choices , width=300, label_visibility="collapsed")
            #if p1:
               # drop_down_choices.remove(p1)
        with col2:
            p2 = st.selectbox("Team 2",placeholder="Team 2",options = drop_down_choices , width=300, label_visibility="collapsed")
            #if p2:
                #drop_down_choices.remove(p2)
        with col3:
            crt = st.selectbox("Court", width=75, options=[1,2,3,4,5,6,7,8,9], label_visibility="collapsed", placeholder="Court")
        with col4:
            submit=st.form_submit_button("Add Match")
        if p1 and p2 and crt and submit:
            c.execute("""
                INSERT INTO matches 
                (player1, player2, court,
                    s1_p1, s1_p2,
                    s2_p1, s2_p2,
                    s3_p1, s3_p2,
                    last_updated, is_new)
                VALUES (?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0)
            """, (p1, p2, crt))
            conn.commit()
            st.success("Match added")
            st.rerun()