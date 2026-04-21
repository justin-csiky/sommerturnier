import streamlit as st
import sqlite3
from datetime import datetime

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

# --- ADMIN PASSWORD ---
ADMIN_PASSWORD = "admin123"

# --- SESSION STATE ---
if "admin" not in st.session_state:
    st.session_state.admin = False

if "selected_match" not in st.session_state:
    st.session_state.selected_match = None

st.title("🏸 Badminton Tournament")

# --- HELPER ---
def parse_score(value):
    try:
        return int(value)
    except:
        return 0

# --- SIDEBAR ---
with st.sidebar:
    st.header("Admin Mode")

    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state.admin = True
            st.success("Admin mode enabled")
        else:
            st.error("Wrong password")

    if st.session_state.admin:
        if st.button("Logout"):
            st.session_state.admin = False

        # 🔄 REFRESH BUTTON
        if st.button("🔄 Refresh"):
            st.rerun()

# --- ADMIN PANEL ---
if st.session_state.admin:
    st.subheader("➕ Add Match")

    p1 = st.text_input("Player 1")
    p2 = st.text_input("Player 2")
    crt = st.text_input("Court")

    if st.button("Add Match"):
        if p1 and p2 and crt:
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

# --- FETCH MATCHES ---
matches = c.execute("""
SELECT id, player1, player2, court,
       s1_p1, s1_p2,
       s2_p1, s2_p2,
       s3_p1, s3_p2,
       last_updated, is_new
FROM matches
""").fetchall()

# =========================================================
# 🏠 HOME VIEW (MATCH LIST)
# =========================================================
if st.session_state.selected_match is None:

    st.subheader("📋 Matches")

    for match in matches:
        match_id, p1, p2, crt, *rest = match
        is_new = rest[-1]

        title = f"{p1} vs {p2} on Court {crt}"

        if is_new and st.session_state.admin:
            title += " 🆕"

        if st.button(title, key=f"open_{match_id}"):
            st.session_state.selected_match = match_id
            st.rerun()

# =========================================================
# 📄 MATCH DETAIL VIEW
# =========================================================
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

    st.subheader(f"{p1} vs {p2}")

    # --- BACK BUTTON ---
    if st.button("⬅ Back"):
        st.session_state.selected_match = None
        st.rerun()

    # --- SET INPUTS ---
    st.write("**Set 1**")
    col1, col2 = st.columns(2)
    with col1:
        set1_p1 = parse_score(st.text_input(
            f"{p1} points",
            value=str(s1p1) if s1p1 else "",
            key="s1p1"
        ))
    with col2:
        set1_p2 = parse_score(st.text_input(
            f"{p2} points",
            value=str(s1p2) if s1p2 else "",
            key="s1p2"
        ))

    st.write("**Set 2**")
    col1, col2 = st.columns(2)
    with col1:
        set2_p1 = parse_score(st.text_input(
            f"{p1} points ",
            value=str(s2p1) if s2p1 else "",
            key="s2p1"
        ))
    with col2:
        set2_p2 = parse_score(st.text_input(
            f"{p2} points ",
            value=str(s2p2) if s2p2 else "",
            key="s2p2"
        ))

    st.write("**Set 3 (optional)**")
    col1, col2 = st.columns(2)
    with col1:
        set3_p1_raw = st.text_input(
            f"{p1} points  ",
            value=str(s3p1) if s3p1 else "",
            key="s3p1"
        )
        set3_p1 = parse_score(set3_p1_raw)

    with col2:
        set3_p2_raw = st.text_input(
            f"{p2} points  ",
            value=str(s3p2) if s3p2 else "",
            key="s3p2"
        )
        set3_p2 = parse_score(set3_p2_raw)

    # --- SUBMIT ---
    if st.button("Submit Result"):

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

        st.success("Result submitted")

    # --- DELETE (ADMIN) ---
    if st.session_state.admin:
        if st.button("🗑️ Delete Match"):
            c.execute("DELETE FROM matches WHERE id=?", (match_id,))
            conn.commit()
            st.session_state.selected_match = None
            st.rerun()

    # --- MARK AS SEEN ---
    if st.session_state.admin and is_new:
        c.execute("UPDATE matches SET is_new=0 WHERE id=?", (match_id,))
        conn.commit()