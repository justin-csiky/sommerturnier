import streamlit as st
from streamlit_theme import st_theme
import sqlite3
from datetime import datetime

# --- UI CLEANUP ---
st.markdown("""
<style>
    [data-testid="stMainMenu"] {display: none;}
    [data-testid="stToolbarActions"] {display: none;}
    [data-testid="appCreatorAvatar"] {display: none;}
    [data-testid="manage-app-button"] {display: none;}
    [class="_container_gzau3_1 _viewerBadge_aycw8_23"] {display: none;}
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
st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
if st.session_state.language== "german":
    st.title("Sommerturnier - V1.13.4",anchor=False)
elif st.session_state.language== "english":
    st.title("Summer tourney - V1.13.4",anchor=False)
#st.markdown("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>", unsafe_allow_html=True)
with st.container(border=True,width=1000):
    if st.session_state.language == "english":
        st.markdown('''<div style="pointer-events: none">
                            <h3>
                                Welcome to the summer tourney website!
                            </h3>  
                        </div>
                        <div style="line-height:2;">
                            <div style="line-height:.75;">
                                <br></br>
                            </div>
                            <div style="pointer-events: none">
                                <u>
                                    <h6>
                                        How you use the website:
                                    </h6>
                                </u>
                            </div>
                            <div style="line-height:.25;">
                                <br></br>
                            </div>
                            <div>In the <span style="color:#1c83e1;">sidebar</span>, you can find a link to informations about all ongoing games. Additionally, you can find the different tourney classes there, with informations about the groups, the current placements and the K/O tree.
                            </div>
                            <div style="line-height:1;">
                                <br></br>
                            </div>                          
                            <div style="pointer-events: none">
                                <u>
                                    <h6>
                                        Tourney infos:
                                    </h6>
                                </u>
                            </div>
                            <div>
                                Please register your team at the front desk <span style="color:#1c83e1;">no later than 10 minutes</span> before the start time specified in the schedule.
                                <div style="line-height:.5;">
                                    <br></br>
                                </div>
                                In the <span style="color:#1c83e1;">Level 1<span>&#x2f;</span>2</span> and <span style="color:#1c83e1;">Men's doubles</span>, we play a group stage with four groups. 
                                The top two team from each group advance to the quaterfinals. For <span style="color:#1c83e1;">mixed doubles</span>, we play every game, due to the few teams. The <span style="color:#1c83e1;">women's doubles</span> play together with the men's doubles, but get placed separately.
                                <div style="line-height:.5;">
                                    <br></br>
                                </div>
                                All matches are played as best<span>&ndash;</span>of<span>&ndash;</span>three sets. 
                                Due to the temperatures, we will play <span style="color:#1c83e1;">sets to 15</span> with an overtime period up to a <span style="color:#1c83e1;">maximum of 17</span> points.
                            </div>
                            <div style="line-height:1;">
                                <br></br>
                            </div>                          
                            <div style="pointer-events: none">
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
                                09:00<span>&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&nbsp&nbsp&nbsp</span>Welcome words                       
                            </div>
                            <div>
                                09:00 <span>&ndash;</span> 14:00<span>&emsp;&emsp;</span>Level 1<span>&#x2f;</span>2 and mixed doubles                       
                            </div>
                            <div>
                                14:00 <span>&ndash;</span> 14:30<span>&emsp;&emsp;</span>Victory ceremony (Level 1<span>&#x2f;</span>2 and mixed)                      
                            </div>
                            <div>
                                14:30 <span>&ndash;</span> 18:00<span>&emsp;&emsp;</span>Men's and Women's doubles
                            </div>
                            <div>
                                18:00 <span>&ndash;</span> 18:15<span>&emsp;&emsp;</span>Victory ceremony (Men's and Women's doubles)
                            </div>
                            <div style="line-height:1;">
                                <br></br>
                            </div>  
                        </div>      
                    ''', unsafe_allow_html=True)
    if st.session_state.language == "german":
        st.markdown('''<div style="pointer-events: none">
                            <h3>
                                Wilkommen auf der Sommerturnier<span>&ndash;</span>Website!
                            </h3>  
                        </div>
                        <div style="line-height:2;">
                            <div style="line-height:.75;">
                                <br></br>
                            </div>
                            <div style="pointer-events: none">
                                <u>
                                    <h6>
                                        Wie ihr die Website nutzt:
                                    </h6>
                                </u>
                            </div>
                            <div style="line-height:.25;">
                                <br></br>
                            </div>
                            <div>In der <span style="color:#1c83e1;">Seitenleiste</span> findet einen Link zu Infos über alle laufenden Spiele. Zusätzlich findet ihr dort die verschiedenen Turnierklassen, wo ihr die verschiedenen Gruppen, die momentanen Platzierungen und den Finalbaum einsehen könnt.
                            </div>
                            <div style="line-height:1;">
                                <br></br>
                            </div>                          
                            <div style="pointer-events: none">
                                <u>
                                    <h6>
                                        Turnier<span>&ndash;</span>Infos:
                                    </h6>
                                </u>
                            </div>
                            <div>
                                Bitte meldet euer Team <span style="color:#1c83e1;">bis 10 Minuten</span> vor Beginn der im Zeitplan angegeben Zeit bei der Turnierleitung an.
                                <div style="line-height:.5;">
                                    <br></br>
                                </div>
                                In den Klassen <span style="color:#1c83e1;">Level 1<span>&#x2f;</span>2</span> und <span style="color:#1c83e1;">Herrendoppel</span> spielen wir eine Gruppenphase mit vier Gruppen. 
                                Die ersten beiden Teams jeder Gruppe ziehen ins Viertelfinale ein. In der Klasse <span style="color:#1c83e1;">Mixed</span> spielen wir aufgrund der wenigen Anmeldungen alle Spiele aus. Die <span style="color:#1c83e1;">Damendoppel</span> spielen mit den Herrendoppeln zusammen, werden aber separat gewertet.
                                <div style="line-height:.5;">
                                    <br></br>
                                </div>
                                Alle Spiele werden bis zwei Gewinnsätze gespielt. 
                                Aufgrund der Temperaturen spielen wir die <span style="color:#1c83e1;">Sätze bis 15</span>, mit einer Verlängerung bis <span style="color:#1c83e1;">maximal 17</span> Punkten.
                            </div>
                            <div style="line-height:1;">
                                <br></br>
                            </div>                          
                            <div style="pointer-events: none">
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
                                09:00<span>&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&nbsp&nbsp&nbsp</span>Begrüßung                       
                            </div>
                            <div>
                                09:00 <span>&ndash;</span> 14:00<span>&emsp;&emsp;</span>Level 1<span>&#x2f;</span>2 und Mixed                       
                            </div>
                            <div>
                                14:00 <span>&ndash;</span> 14:30<span>&emsp;&emsp;</span>Siegerehrung (Level 1<span>&#x2f;</span>2 und Mixed)                      
                            </div>
                            <div>
                                14:30 <span>&ndash;</span> 18:00<span>&emsp;&emsp;</span>Herren<span>&#8211;</span> und Damendoppel
                            </div>
                            <div>
                                18:00 <span>&ndash;</span> 18:15<span>&emsp;&emsp;</span>Siegerehrung (Herren<span>&#8211;</span> und Damendoppel)
                            </div>
                            <div style="line-height:1;">
                                <br></br>
                            </div>  
                        </div>      
                    ''', unsafe_allow_html=True)
print(st.theme)