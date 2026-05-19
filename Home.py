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

st.set_page_config(page_title="Sommerturnier",initial_sidebar_state="expanded",layout="wide",page_icon=":badminton:")
home=st.Page("./Home.py",title="Home",icon=":material/dashboard:")
admin=st.Page("./pages/10_Admin_login.py",title="Admin",icon=":material/admin_panel_settings:")

# --- DATABASE SETUP ---
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

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
    is_visible INTEGER DEFAULT 1,
    match_class TEXT
)
""")
conn.commit()
c.execute("""
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    wins INTEGER,
    loses INTEGER,
    wpoints INTEGER,
    lpoints INTEGER,
    class TEXT,
    team_group TEXT,
    group_placement INTEGER
)
""")
conn.commit()
c.execute("""
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class TEXT,
    group_name TEXT,
    is_done INTEGER DEFAULT 0
)
""")
conn.commit()
# --- SESSION STATE ---
if "admin" not in st.session_state:
    st.session_state.admin = False
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None
if "stt" not in st.session_state:
    st.session_state.stt = False 
if "language" not in st.session_state:
    st.session_state.language = "german"


with st.container(horizontal=True):
    if st.button("🇩🇪"):
        st.session_state.language="german"
        st.rerun()
    if st.button("🇬🇧"):
        st.session_state.language="english"
        st.rerun()
    st.space("stretch")
st.title("Sommerturnier - V1.4.1",anchor=False)
st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")
with st.container(border=True,width=700):
    if st.session_state.language == "english":
        st.markdown("Welcome to the summer tournament website")
    if st.session_state.language == "german":
        st.markdown('''<div>
                            <h3>
                                Wilkommen auf der Sommerturnier<span>&ndash;</span>Website!
                            </h3>  
                        </div>
                        <div style="line-height:2;">
                            <div style="line-height:.75;">
                                <br></br>
                            </div>
                            <div>
                                <u>
                                    <h6>
                                        Wie ihr die Website nutzt:
                                    </h6>
                                </u>
                            </div>
                            <div style="line-height:.25;">
                                <br></br>
                            </div>
                            <div>In der <span style="color:#1c83e1;">Seitenleiste</span> findet ihr neben den verschiedenen Klassen einen Link zu allen laufenden Spielen. 
                                Nachdem die Spiele ausgerufen werden, könnt ihr sie dort einsehen und nach Ende des Spiels eure Ergebnisse eintragen.
                                Bitte beachtet, dass die Ergebnisse nach Abgabe nurnoch bei der Turnierleitung geändert werden können.<br></br>
                                Unter den verschiedenen Klassen könnt ihr die Punkte von euch und euren Gegnern beobachten, sowie den Finalbaum einsehen.
                            </div>
                            <div style="line-height:1;">
                                <br></br>
                            </div>                          
                            <div>
                                <u>
                                    <h6>
                                        Turnier<span>&ndash;</span>Infos:
                                    </h6>
                                </u>
                            </div>
                            <div>
                                Bitte meldet euer Team <span style="color:#1c83e1;">bis 10 Minuten</span> vor Beginn der im Zeitplan angegeben Zeit bei der Turnierleitung an.<br></br>
                                In den Klassen Level 1<span>&#x2f;</span>2, Mixed und Herrendoppel spielen wir eine <span style="color:#1c83e1;">Gruppenphase</span> mit vier Gruppen. 
                                Die Erstplatzierten jeder Gruppe ziehen ins Halbfinale ein. In der Klasse Damendoppel spielen wir alle Spiele aus.<br></br>
                                Alle Spiele werden in drei Gewinnsätze gespielt. 
                                Aus Zeitgründen spielen wir in der Gruppenphase die <span style="color:#1c83e1;">Sätze bis 15</span>, mit einer Verlängerung bis maximal 17 Punkten.               
                                <span style="color:#1c83e1;">Ab dem Halbfinale</span> werden Sätze wie üblich <span style="color:#1c83e1;">bis 21</span> gespielt.
                            </div>
                            <div style="line-height:1;">
                                <br></br>
                            </div>                          
                            <div>
                                <u>
                                    <h6>
                                        Zeitplan:
                                    </h6>
                                </u>
                            </div>
                            <div style="line-height:.25;">
                                <br></br>
                            </div>
                            <div>
                                09:00 <span>&ndash;</span> 14:15 Level 1<span>&#x2f;</span>2 und Mixed                       
                            </div>
                            <div>
                                14:45 <span>&ndash;</span> 19:00 Herren<span>&#8211;</span> und Damendoppel
                            </div>
                        </div>      
                    ''', unsafe_allow_html=True)