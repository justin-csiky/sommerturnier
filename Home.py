import streamlit as st
import sqlite3
from datetime import datetime

# --- UI CLEANUP ---
st.markdown("""
<style>
    [data-testid="stMainMenu"] {display: none;}
    [data-testid="stToolbarActions"] {display: none;}
    [data-testid="appCreatorAvatar"] {display: none;}
    [data-testid="manage-app-button"] {display: none;}
    footer {display: none;}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Sommerturnier",initial_sidebar_state="expanded",layout="wide",page_icon=":badminton:")
home=st.Page("./Home.py",title="Home",icon=":material/dashboard:")
admin=st.Page("./pages/10_Admin_login.py",title="Admin",icon=":material/admin_panel_settings:")

# --- DATABASE SETUP ---
conn = sqlite3.connect("matches.db", check_same_thread=False)
c = conn.cursor()

stats = sqlite3.connect("teamstats.db", check_same_thread=False)
s = stats.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player1_id INTEGER,
    player2_id INTEGER,
    court INTEGER,
    s1_p1 INTEGER,
    s1_p2 INTEGER,
    s2_p1 INTEGER,
    s2_p2 INTEGER,
    s3_p1 INTEGER,
    s3_p2 INTEGER,
    last_updated TIMESTAMP,
    is_new INTEGER DEFAULT 0,
    is_visible INTEGER DEFAULT 0,
    match_class STRING
)
""")

s.execute("""
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    wins INTEGER,
    loses INTEGER,
    wpoints INTEGER,
    lpoints INTEGER,
    class STRING
)
""")

conn.commit()
stats.commit()

# --- SESSION STATE ---
if "admin" not in st.session_state:
    st.session_state.admin = False
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None
if "stt" not in st.session_state:
    st.session_state.stt = False

st.title("Sommerturnier - V1.1",anchor=False)

# --- HELPERS ---
def parse_score(v):
    try:
        return int(v)
    except:
        return 0
    
def display_value(x):
    return "" if x is None else str(x)

def get_team_name(team_id):
    res = s.execute("SELECT name FROM teams WHERE id=?", (team_id,)).fetchone()
    return res[0] if res else "Unknown"

# --- RECOMPUTE STATS ---
def recompute_team_stats():
    s.execute("UPDATE teams SET wins=0, loses=0, wpoints=0, lpoints=0")
    stats.commit()

    matches = c.execute("""
        SELECT player1_id, player2_id,
               s1_p1, s1_p2,
               s2_p1, s2_p2,
               s3_p1, s3_p2
        FROM matches
    """).fetchall()

    for m in matches:
        p1, p2, s1p1, s1p2, s2p1, s2p2, s3p1, s3p2 = m

        if None in (s1p1, s1p2, s2p1, s2p2):
            continue

        sets1 = sets2 = 0

        for a, b in [(s1p1, s1p2), (s2p1, s2p2), (s3p1, s3p2)]:
            if a is None or b is None:
                continue
            if a > b:
                sets1 += 1
            else:
                sets2 += 1

        if sets1 > sets2:
            s.execute("UPDATE teams SET wins=wins+1 WHERE id=?", (p1,))
            s.execute("UPDATE teams SET loses=loses+1 WHERE id=?", (p2,))
        else:
            s.execute("UPDATE teams SET wins=wins+1 WHERE id=?", (p2,))
            s.execute("UPDATE teams SET loses=loses+1 WHERE id=?", (p1,))

        s.execute("UPDATE teams SET wpoints=wpoints+? WHERE id=?", (sets1, p1))
        s.execute("UPDATE teams SET lpoints=lpoints+? WHERE id=?", (sets2, p1))
        s.execute("UPDATE teams SET wpoints=wpoints+? WHERE id=?", (sets2, p2))
        s.execute("UPDATE teams SET lpoints=lpoints+? WHERE id=?", (sets1, p2))

    stats.commit()

# =========================================================
# ADMIN PANEL
# =========================================================
if st.session_state.admin and st.session_state.selected_match is None:

    st.subheader(":material/Add_2: Add Team", anchor=False)

    with st.form("add_team", clear_on_submit=True,border=False):
        with st.container(horizontal=True):
            name = st.text_input("Team Name",width=200,label_visibility="collapsed",placeholder="Team Name")
            klasse = st.selectbox("Klasse", ["MX","HD","DD","LVL1/2"],width=200, label_visibility="collapsed", placeholder="Klasse", index=None)
            st.space("stretch")
            submit = st.form_submit_button(":material/Add_Circle:\u00A0\u00A0Add",width=100)
        if submit:
            if not name:
                st.error("Enter name")
            else:
                exists = s.execute("SELECT id FROM teams WHERE name=?", (name,)).fetchone()
                if exists:
                    st.error("Team exists")
                else:
                    s.execute("""
                        INSERT INTO teams (name, wins, loses, wpoints, lpoints, class)
                        VALUES (?,0,0,0,0,?)
                    """, (name,klasse))
                    stats.commit()
                    st.success("Team added")
                    st.rerun()
    st.divider()

    st.subheader(":material/Delete: Delete Team", anchor=False)

    teams = s.execute("SELECT id, name FROM teams").fetchall()

    team_names = [t[1] for t in teams]
    team_dict = {t[1]: t[0] for t in teams}
    with st.container(horizontal=True,border=False):
        team_to_delete = st.selectbox("Select team", team_names,width=200, label_visibility="collapsed",placeholder="Select Team",index=None)
        st.space("stretch")
        if st.button(":material/do_not_disturb_on: Delete",width=100):
            team_id = team_dict[team_to_delete]

            # check if used in matches
            used = c.execute("""
                SELECT 1 FROM matches
                WHERE player1_id=? OR player2_id=?
                LIMIT 1
            """, (team_id, team_id)).fetchone()

            if used:
                st.warning("Team is used in matches")

                if st.button("Force delete (danger)"):
                    c.execute("""
                        DELETE FROM matches
                        WHERE player1_id=? OR player2_id=?
                    """, (team_id, team_id))
                    conn.commit()

                    s.execute("DELETE FROM teams WHERE id=?", (team_id,))
                    stats.commit()

                    recompute_team_stats()

                    st.success("Team and related matches deleted")
                    st.rerun()
            else:
                s.execute("DELETE FROM teams WHERE id=?", (team_id,))
                stats.commit()
                st.success("Team deleted")
                st.rerun()
    st.divider()
    st.subheader(":material/Add_2: Add Match", anchor=False)

    teams = s.execute("SELECT id, name, class FROM teams").fetchall()
    team_dict = {name: tid for tid, name, klasse in teams}
    team_klasse = {name: klasse for tid, name, klasse in teams}
    names = list(team_dict.keys())

    with st.form("add_match", clear_on_submit=False, border=False):
        with st.container(horizontal=True,border=False, vertical_alignment="center",key="first"):
            p1_name = st.selectbox("Team 1", names,width=200,placeholder="Team 1", index=None)
            p2_name = st.selectbox("Team 2", names,width=200,placeholder="Team 2", index=None)
            court = st.selectbox("Court", list(range(1,10)), width=100,placeholder="Court", index=None)
            st.space("stretch")
            submit = st.form_submit_button(":material/Add_Circle:\u00A0\u00A0Add",width=100)
        if submit:                
            if team_klasse[p1_name]==team_klasse[p2_name]:
                c.execute("""
                    INSERT INTO matches (player1_id, player2_id, court, match_class)
                    VALUES (?, ?, ?, ?)
                """, (team_dict[p1_name], team_dict[p2_name], court, team_klasse[p1_name]))
                conn.commit()
                st.success("Match added")
                st.rerun()
            else:
                st.warning("Nicht in der gleichen Gruppe.")
            
                    

# =========================================================
# MATCH LIST
# =========================================================
matches = c.execute("""
SELECT id, player1_id, player2_id, court, last_updated, is_visible
FROM matches
""").fetchall()

if st.session_state.selected_match is None:

    st.subheader("Matches", anchor=False)

    for m in matches:
        mid, p1, p2, court, updated, visible = m
        if visible or st.session_state.admin:    
            name1 = get_team_name(p1)
            name2 = get_team_name(p2)
            with st.container(horizontal=True,border=False, vertical_alignment="center"):
                st.markdown(f"On Court {court}:")
                if st.button(f"***{name1}*** vs ***{name2}***", key=f"open_{mid}",width=350,):
                    st.session_state.selected_match = mid
                    st.rerun()
                st.space("stretch")
                if st.session_state.admin and visible:
                    if st.button(":material/Visibility_Off:", key=f"vis_match_{mid}"):
                        c.execute("UPDATE matches SET is_visible=? WHERE id=?", (0,mid))
                        conn.commit()
                        st.rerun()
                elif st.session_state.admin and not visible:
                    if st.button(":material/Visibility:", key=f"vis_match_{mid}"):
                        c.execute("UPDATE matches SET is_visible=? WHERE id=?", (1,mid))
                        conn.commit()
                        st.rerun()
                if st.session_state.admin:
                    if st.button(":material/Delete:", key=f"del_match_{mid}"):
                        c.execute("DELETE FROM matches WHERE id=?", (mid,))
                        conn.commit()

                        recompute_team_stats()

                        st.success("Match deleted")
                        st.rerun()


# =========================================================
# MATCH DETAIL
# =========================================================
else:
    mid = st.session_state.selected_match

    m = c.execute("""
    SELECT * FROM matches WHERE id=?
    """, (mid,)).fetchone()

    (_, p1, p2, court,
     s1p1, s1p2, s2p1, s2p2, s3p1, s3p2,
     last_updated,is_visible, klasse, _) = m

    name1 = get_team_name(p1)
    name2 = get_team_name(p2)

    st.subheader(f"***{name1}*** vs ***{name2}***",anchor=False)
    with st.container(horizontal=True):
        st.space("stretch")
        if st.button(":material/undo: Back",width=100):
            st.session_state.selected_match = None
            st.rerun()

    is_locked = last_updated is not None and not st.session_state.admin
    with st.container(horizontal=True):
        st.space("stretch")
        with st.form("result_form", width=700):
            with st.container(horizontal=True):
                # --- SET 1 ---
                with st.container():
                    with st.container(horizontal=True,width=300):
                        st.space("stretch")
                        st.markdown("1. Set",text_alignment="center")
                        st.space("stretch")
                    with st.container(horizontal=True,width=300):
                        st.space("stretch")
                        s1a = parse_score(st.text_input(
                            "Set1 Team1",width=50,label_visibility="collapsed",
                            value=str(s1p1) if s1p1 is not None else ""
                        ))
                        st.markdown(":",text_alignment="center")
                        s1b = parse_score(st.text_input(
                            "Set1 Team2",width=50,label_visibility="collapsed",
                            value=str(s1p2) if s1p2 is not None else ""
                        ))
                        st.space("stretch")

                # --- SET 2 ---
                with st.container():
                    with st.container(horizontal=True,width=300):
                        st.space("stretch")
                        st.markdown("2. Set",text_alignment="center")
                        st.space("stretch")
                    with st.container(horizontal=True,width=300):
                        st.space("stretch")
                        s2a = parse_score(st.text_input(
                            "Set2 Team1",width=50,label_visibility="collapsed",
                            value=str(s2p1) if s2p1 is not None else ""
                        ))
                        st.markdown(":",text_alignment="center")
                        s2b = parse_score(st.text_input(
                            "Set2 Team2",width=50,label_visibility="collapsed",
                            value=str(s2p2) if s2p2 is not None else ""
                        ))
                        st.space("stretch")

                # --- SET 3 ---
                with st.container():
                    with st.container(horizontal=True,width=300):
                        st.space("stretch")
                        st.markdown("3. Set",text_alignment="center")
                        st.space("stretch")
                    with st.container(horizontal=True,width=300):
                        st.space("stretch")
                        s3a_raw = st.text_input(
                            "Set3 Team1",width=50,label_visibility="collapsed",
                            value=str(s3p1) if s3p1 is not None else ""
                        )
                        st.markdown(":",text_alignment="center")
                        s3b_raw = st.text_input(
                            "Set3 Team2",width=50,label_visibility="collapsed",
                            value=str(s3p2) if s3p2 is not None else ""
                        )
                        st.space("stretch")

            s3a = parse_score(s3a_raw)
            s3b = parse_score(s3b_raw)
            with st.container(horizontal=True):
                st.space("stretch")
                submit = st.form_submit_button("Verbindlich abgeben", disabled=is_locked,width=200)
                st.space("stretch")
        st.space("stretch")
        if submit:

            # --- detect if set 3 was played ---
            if s3a_raw.strip() == "" and s3b_raw.strip() == "":
                s3a_val = None
                s3b_val = None
            else:
                s3a_val = s3a
                s3b_val = s3b

            c.execute("""
                UPDATE matches SET
                s1_p1=?, s1_p2=?,
                s2_p1=?, s2_p2=?,
                s3_p1=?, s3_p2=?,
                last_updated=?
                WHERE id=?
            """, (s1a, s1b, s2a, s2b, s3a_val, s3b_val, datetime.now(), mid))

            conn.commit()

            recompute_team_stats()

            st.success("Saved")
            st.rerun()
    with st.container(horizontal=True):
        st.space("stretch")
        if is_locked:
                st.warning("Ergebnisse abgegeben.",width=200)
        st.space("stretch")
with st.container(horizontal=True):
    st.space("stretch")
    if st.button(":material/refresh: Reload",width=100):
        st.rerun()