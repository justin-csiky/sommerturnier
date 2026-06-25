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
    match_class TEXT,
    stage TEXT
)
""")
conn.commit()
c.execute("""
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    wins INTEGER DEFAULT 0,
    loses INTEGER DEFAULT 0,
    wsets INTEGER DEFAULT 0,
    lsets INTEGER DEFAULT 0,
    wpoints INTEGER DEFAULT 0,
    lpoints INTEGER DEFAULT 0,
    total_wins INTEGER DEFAULT 0,
    total_loses INTEGER DEFAULT 0,
    total_wsets INTEGER DEFAULT 0,
    total_lsets INTEGER DEFAULT 0,
    total_wpoints INTEGER DEFAULT 0,
    total_lpoints INTEGER DEFAULT 0,
    class TEXT,
    team_group TEXT,
    group_placement INTEGER DEFAULT 0,
    quaters_nr_winner INTEGER DEFAULT 0,
    semis_nr_winner INTEGER DEFAULT 0,
    third_place INTEGER DEFAULT 0,
    semis_nr_loser INTEGER DEFAULT 0,
    finals_winner INTEGER DEFAULT 0
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
c.execute("""
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class TEXT,
    group_number INTEGER DEFAULT 4,    
    which_third_is_missing INTEGER DEFAULT 0     
)
""")
conn.commit()
settings = c.execute("SELECT id, group_number FROM settings").fetchall()
number=c.execute("SELECT Count(id) FROM settings").fetchall()
if not number[0][0]==4:
    c.execute("DELETE FROM settings")
    c.execute("INSERT INTO settings (class) VALUES (?)",('LVL1/2',))
    c.execute("INSERT INTO settings (class) VALUES (?)",('MX',))
    c.execute("INSERT INTO settings (class) VALUES (?)",('DD',))
    c.execute("INSERT INTO settings (class) VALUES (?)",('HD',))
    conn.commit()
# --- SESSION STATE ---
if "admin" not in st.session_state:
    st.session_state.admin = False
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None
if "language" not in st.session_state:
    st.session_state.language = "german"
if "input_mode" not in st.session_state:
    st.session_state.input_mode = False


with st.container(horizontal=True):
    if st.button("🇩🇪"):
        st.session_state.language="german"
        st.rerun()
    if st.button("🇬🇧"):
        st.session_state.language="english"
        st.rerun()
    st.space("stretch")
st.title("Sommerturnier - V1.12.1",anchor=False)
#st.markdown("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>", unsafe_allow_html=True)
with st.container(border=True,width=1000):
    if st.session_state.language == "english":
        st.markdown('''<div>
                            <h3>
                                Welcome to the summer tourney website!
                            </h3>  
                        </div>
                        <div style="line-height:2;">
                            <div style="line-height:.75;">
                                <br></br>
                            </div>
                            <div>
                                <u>
                                    <h6>
                                        How you use the website:
                                    </h6>
                                </u>
                            </div>
                            <div style="line-height:.25;">
                                <br></br>
                            </div>
                            <div>In the <span style="color:#1c83e1;">sidebar</span>, you will find a link to all ongoing games, in addition to the different classes. 
                                Once the games are announced, you can view them there and enter your results after the game has ended.
                                Please note that once submitted, results can only be changed by going to the front desk.<br></br>
                                Under the different classes you can observe your and your opponents' points, as well as view the final bracket.
                            </div>
                            <div style="line-height:1;">
                                <br></br>
                            </div>                          
                            <div>
                                <u>
                                    <h6>
                                        Tourney infos:
                                    </h6>
                                </u>
                            </div>
                            <div>
                                Please register your team at the front desk <span style="color:#1c83e1;">no later than 10 minutes</span> before the start time specified in the schedule.<br></br>
                                In the Level 1<span>&#x2f;</span>2, Mixed and Men's doubles, we play a group stage with four groups. 
                                The top team from each group advances to the semifinals. In the women's doubles category, we play all matches.<br></br>
                                All matches are played as best<span>&ndash;</span>of<span>&ndash;</span>three sets. 
                                Due to time constraints, we will play <span style="color:#1c83e1;">sets to 15</span> in the group stage, with an overtime period up to a maximum of 17 points.
                                <span style="color:#1c83e1;">From the semi-finals onwards</span>, sets are played as usual <span style="color:#1c83e1;">to 21</span>.
                            </div>
                            <div style="line-height:1;">
                                <br></br>
                            </div>                          
                            <div>
                                <u>
                                    <h6>
                                        Schedule:
                                    </h6>
                                </u>
                            </div>
                            <div style="line-height:.25;">
                                <br></br>
                            </div>
                            <div>
                                09:00 <span>&ndash;</span> 14:15 Level 1<span>&#x2f;</span>2 and Mixed                       
                            </div>
                            <div>
                                14:45 <span>&ndash;</span> 19:00 Men's and Women's doubles
                            </div>
                        </div>      
                    ''', unsafe_allow_html=True)
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
                                Alle Spiele werden in zwei Gewinnsätze gespielt. 
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