import streamlit as st
import sqlite3
from datetime import datetime
import time
st.markdown("""
<style>
    /* Hide top header, hamburger menu, and footer */
    [data-testid="stHeader"] {display: none;}
    footer {visibility: hidden;}
    
    /* Keep sidebar functional but hide the thin top bar of the sidebar */
    [data-testid="stSidebar"] {
        top: 0;
        height: 100vh;
    }
</style>
""", unsafe_allow_html=True)
# --- DATABASE SETUP ---
conn = sqlite3.connect("tournament.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player1 TEXT,
    player2 TEXT,
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
st.set_page_config(initial_sidebar_state="expanded")
# --- ADMIN PASSWORD ---
ADMIN_PASSWORD = "admin123"

# --- SESSION STATE ---
if "admin" not in st.session_state:
    st.session_state.admin = False

if "selected_match" not in st.session_state:
    st.session_state.selected_match = None

if "new_updates" not in st.session_state:
    st.session_state.new_updates = False

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
        st.subheader("On-going matches:", anchor=False)
        if c.fetchone!=None:
            for match in matches:
                match_id, p1, p2, crt, *rest = match
                is_new = rest[-1]

                title = f"{p1} vs {p2} on Court {crt}"

                if is_new and st.session_state.admin:
                    title += " ‼️"
                col1,ce1,ce2, col2 =st.columns([9,1,1,1])
                with col1:
                    if st.button(title, key=f"open_{match_id}",width=500):
                        st.session_state.selected_match = match_id
                        st.rerun()
                with col2:  
                    if st.session_state.admin:
                        if st.button("🗑️",key=f"del_{match_id}"):
                            c.execute("DELETE FROM matches WHERE id=?", (match_id,))
                            conn.commit()
                            st.session_state.selected_match = None
                            st.rerun()                
                
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

        st.subheader(f"{p1} vs {p2}",anchor=False)
        # --- BACK BUTTON ---
        if st.button("⬅ Back"):
            st.session_state.selected_match = None
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
            c1,c2,c3=st.columns(3,border=True)
            point_cell_width=45
            with c1:
                st.markdown("**Set 1**",text_alignment="center")
                with st.container(horizontal=True,vertical_alignment="center"):
                    set1_p1 = parse_score(st.text_input(
                        f"{shp1}",
                        value=str(s1p1) if s1p1 else "",
                        key="s1p1", width=point_cell_width
                    ))
                    st.space("stretch")
                    st.markdown(":")
                    st.space("stretch")
                    set1_p2 = parse_score(st.text_input(
                        f"{shp2}",
                        value=str(s1p2) if s1p2 else "",
                        key="s1p2", width=point_cell_width
                    ))
            with c2:
                st.markdown("**Set 2**",text_alignment="center")
                with st.container(horizontal=True,vertical_alignment="center"):
                    set2_p1 = parse_score(st.text_input(
                        f"{shp1}",
                        value=str(s2p1) if s2p1 else "",
                        key="s2p13", width=point_cell_width
                    ))
                    st.space("stretch")
                    st.markdown(":")
                    st.space("stretch")
                    set2_p2 = parse_score(st.text_input(
                        f"{shp2}",
                        value=str(s2p2) if s2p2 else "",
                        key="s2p2", width=point_cell_width
                    ))
            with c3:
                st.markdown("**Set 3 (optional)**",text_alignment="center")
                with st.container(horizontal=True,vertical_alignment="center"):
                    set3_p1_raw = st.text_input(
                        f"{shp1}",
                        value=str(s3p1) if s3p1 else "",
                        key="s3p1", width=point_cell_width
                    )
                    set3_p1 = parse_score(set3_p1_raw)
                    st.space("stretch")
                    st.markdown(":")
                    st.space("stretch")
                    set3_p2_raw = st.text_input(
                        f"{shp2}",
                        value=str(s3p2) if s3p2 else "",
                        key="s3p2", width=point_cell_width
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
adminlogin=st.Page("./pages/1_Admin_login.py", title="Login", icon=":material/login:")
matchview=st.Page(view_matches(1), title="Match Overview")

# --- SIDEBAR ---
with st.sidebar:
    # 🔄 REFRESH BUTTON
    if st.button("🔄 Refresh"):
        st.rerun()

# --- ADMIN PANEL ---
if st.session_state.admin and not st.session_state.selected_match:
    st.subheader("➕ Add Match", anchor=False)
    with st.form('add_match_form',clear_on_submit=True):
        col1, col2, col3, col4 = st.columns([2,2,1,1])
        with col1:
            p1 = st.text_input("Player 1",placeholder="Team 1", width=300, label_visibility="collapsed")
        with col2:
            p2 = st.text_input("Player 2",placeholder="Team 2", width=300, label_visibility="collapsed")
        with col3:
            crt = st.text_input("Court", width=75, label_visibility="collapsed", placeholder="Court")
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