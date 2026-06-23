import streamlit as st
import sqlite3
from datetime import datetime
if "admin" not in st.session_state:
    st.session_state.admin = False
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None
if "language" not in st.session_state:
    st.session_state.language = "german"
if "input_mode" not in st.session_state:
    st.session_state.input_mode = False
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
# --- HELPERS ---
def parse_score(v):
    try:
        return int(v)
    except:
        return 0
    
def display_value(x):
    return "" if x is None else str(x)

def get_team_name(team_id):
    res = c.execute("SELECT name FROM teams WHERE id=?", (team_id,)).fetchone()
    return res[0] if res else "Unknown"

def get_team_group(team_id):
    res = c.execute("SELECT team_group FROM teams WHERE id=?", (team_id,)).fetchone()
    return res[0] if res else "Unknown"

def get_team_placement(team_id):
    res = c.execute("SELECT group_placement FROM teams WHERE id=?", (team_id,)).fetchone()
    return res[0] if res else "Unknown"

# --- RECOMPUTE STATS ---
def recompute_team_stats(mid, stage_name="Quaters", old_s1p1=0, old_s1p2=0, old_s2p1=0, old_s2p2=0, old_s3p1=0, old_s3p2=0):
    sets1 = sets2 = 0
    total_points_1 = old_s1p1 + old_s2p1 + old_s3p1
    total_points_2 = old_s1p2 + old_s2p2 + old_s3p2
    match = c.execute("SELECT player1_id, player2_id, s1_p1, s1_p2, s2_p1, s2_p2, s3_p1, s3_p2 FROM matches WHERE id=?", (mid,)).fetchone()
    (p1, p2, s1p1, s1p2, s2p1, s2p2, s3p1, s3p2) = match
    for a, b in [(old_s1p1, old_s1p2), (old_s2p1, old_s2p2), (old_s3p1, old_s3p2)]:
        if a==0 and b==0:
            continue
        if a > b:
            sets1 += 1
        else:
            sets2 += 1
    if sets1 > sets2:
        c.execute("UPDATE teams SET total_wins=total_wins-1 WHERE id=?", (p1,))
        c.execute("UPDATE teams SET total_loses=total_loses-1 WHERE id=?", (p2,))
        if stage_name == "Bracket":
            c.execute("UPDATE teams SET wins=wins-1 WHERE id=?", (p1,))
            c.execute("UPDATE teams SET loses=loses-1 WHERE id=?", (p2,))
    elif sets1 < sets2:
        c.execute("UPDATE teams SET total_wins=total_wins-1 WHERE id=?", (p2,))
        c.execute("UPDATE teams SET total_loses=total_loses-1 WHERE id=?", (p1,))
        if stage_name == "Bracket":
            c.execute("UPDATE teams SET wins=wins-1 WHERE id=?", (p2,))
            c.execute("UPDATE teams SET loses=loses-1 WHERE id=?", (p1,))
    if stage_name == "Bracket":
        c.execute("UPDATE teams SET wsets=wsets-? WHERE id=?", (sets1, p1))
        c.execute("UPDATE teams SET lsets=lsets-? WHERE id=?", (sets2, p1))
        c.execute("UPDATE teams SET wsets=wsets-? WHERE id=?", (sets2, p2))
        c.execute("UPDATE teams SET lsets=lsets-? WHERE id=?", (sets1, p2))
        c.execute("UPDATE teams SET wpoints=wpoints-? WHERE id=?", (total_points_2, p2))
        c.execute("UPDATE teams SET lpoints=lpoints-? WHERE id=?", (total_points_1, p2))
        c.execute("UPDATE teams SET wpoints=wpoints-? WHERE id=?", (total_points_1, p1))
        c.execute("UPDATE teams SET lpoints=lpoints-? WHERE id=?", (total_points_2, p1))
    c.execute("UPDATE teams SET total_wsets=total_wsets-? WHERE id=?", (sets1, p1))
    c.execute("UPDATE teams SET total_lsets=total_lsets-? WHERE id=?", (sets2, p1))
    c.execute("UPDATE teams SET total_wsets=total_wsets-? WHERE id=?", (sets2, p2))
    c.execute("UPDATE teams SET total_lsets=total_lsets-? WHERE id=?", (sets1, p2))
    c.execute("UPDATE teams SET total_wpoints=total_wpoints-? WHERE id=?", (total_points_2, p2))
    c.execute("UPDATE teams SET total_lpoints=total_lpoints-? WHERE id=?", (total_points_1, p2))
    c.execute("UPDATE teams SET total_wpoints=total_wpoints-? WHERE id=?", (total_points_1, p1))
    c.execute("UPDATE teams SET total_lpoints=total_lpoints-? WHERE id=?", (total_points_2, p1))
    sets1 = sets2 = 0
    if s3p1 is None and s3p2 is None:
        s3p1=0
        s3p2=0
    total_points_1= s1p1+s2p1+s3p1
    total_points_2= s1p2+s2p2+s3p2
    for a, b in [(s1p1, s1p2), (s2p1, s2p2), (s3p1, s3p2)]:
        if a==0 and b==0:
            continue
        if a > b:
            sets1 += 1
        else:
            sets2 += 1
    if sets1 > sets2:
        c.execute("UPDATE teams SET total_wins=total_wins+1 WHERE id=?", (p1,))
        c.execute("UPDATE teams SET total_loses=total_loses+1 WHERE id=?", (p2,))
        if stage_name == "Bracket":
            c.execute("UPDATE teams SET wins=wins+1 WHERE id=?", (p1,))
            c.execute("UPDATE teams SET loses=loses+1 WHERE id=?", (p2,))
        winner=p1
    else:
        c.execute("UPDATE teams SET total_wins=total_wins+1 WHERE id=?", (p2,))
        c.execute("UPDATE teams SET total_loses=total_loses+1 WHERE id=?", (p1,))
        if stage_name == "Bracket":
            c.execute("UPDATE teams SET wins=wins+1 WHERE id=?", (p2,))
            c.execute("UPDATE teams SET loses=loses+1 WHERE id=?", (p1,))
        winner=p2
    if stage_name == "Bracket":
        c.execute("UPDATE teams SET wsets=wsets+? WHERE id=?", (sets1, p1))
        c.execute("UPDATE teams SET lsets=lsets+? WHERE id=?", (sets2, p1))
        c.execute("UPDATE teams SET wsets=wsets+? WHERE id=?", (sets2, p2))
        c.execute("UPDATE teams SET lsets=lsets+? WHERE id=?", (sets1, p2))
        c.execute("UPDATE teams SET wpoints=wpoints+? WHERE id=?", (total_points_2, p2))
        c.execute("UPDATE teams SET lpoints=lpoints+? WHERE id=?", (total_points_1, p2))
        c.execute("UPDATE teams SET wpoints=wpoints+? WHERE id=?", (total_points_1, p1))
        c.execute("UPDATE teams SET lpoints=lpoints+? WHERE id=?", (total_points_2, p1))
    c.execute("UPDATE teams SET total_wsets=total_wsets+? WHERE id=?", (sets1, p1))
    c.execute("UPDATE teams SET total_lsets=total_lsets+? WHERE id=?", (sets2, p1))
    c.execute("UPDATE teams SET total_wsets=total_wsets+? WHERE id=?", (sets2, p2))
    c.execute("UPDATE teams SET total_lsets=total_lsets+? WHERE id=?", (sets1, p2))
    c.execute("UPDATE teams SET total_wpoints=total_wpoints+? WHERE id=?", (total_points_2, p2))
    c.execute("UPDATE teams SET total_lpoints=total_lpoints+? WHERE id=?", (total_points_1, p2))
    c.execute("UPDATE teams SET total_wpoints=total_wpoints+? WHERE id=?", (total_points_1, p1))
    c.execute("UPDATE teams SET total_lpoints=total_lpoints+? WHERE id=?", (total_points_2, p1))
    conn.commit()
    return winner

if st.session_state.admin and st.session_state.selected_match is None and not st.session_state.input_mode:
    with st.container(border=True):
#------------------
#Teams hinzufügen
#------------------
        st.subheader(":material/Add_2: Add Team", anchor=False)
        with st.form("add_team", clear_on_submit=True,border=False):
            with st.container(horizontal=True):
                name = st.text_input("Team Name",width=200,label_visibility="collapsed",placeholder="Team Name")
                klasse = st.selectbox("Klasse", ["MX","HD","DD","LVL1/2"],width=150, label_visibility="collapsed", placeholder="Klasse", index=None)
                gruppe = st.selectbox("Klasse", ["A","B","C","D"],width=100, label_visibility="collapsed", placeholder="Gruppe", index=None)
                st.space("stretch")
                submit = st.form_submit_button(":material/Add_Circle:\u00A0\u00A0Add",width=100)
            if submit:
                if not name:
                    st.error("Enter name")
                else:
                    exists = c.execute("SELECT id FROM teams WHERE name=?", (name,)).fetchone()
                    if exists:
                        st.error("Team exists")
                    else:
                        c.execute("""
                            INSERT INTO teams (name, wins, loses, wsets, lsets, class, team_group, quaters_nr_winner, semis_nr_winner, finals_winner)
                            VALUES (?,0,0,0,0,?,?,0,0,0)
                        """, (name,klasse,gruppe))
                        conn.commit()
                        groupcheck = c.execute("SELECT group_name FROM groups WHERE class=?", (klasse,)).fetchall()
                        checkbit=False
                        for names in groupcheck:
                            if names[0]==gruppe:
                                checkbit=True
                        if not checkbit:
                            c.execute("""
                                INSERT INTO groups (class, group_name, is_done)
                                VALUES (?,?,?)
                            """, (klasse,gruppe,0))
                            conn.commit()
                        st.rerun()
        st.divider()
#------------------
#Teams löschen
#------------------
        st.subheader(":material/Delete: Delete Team", anchor=False)
        teams = c.execute("SELECT id, name FROM teams").fetchall()
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
                        c.execute("DELETE FROM teams WHERE id=?", (team_id,))
                        conn.commit()
                        st.success("Team and related matches deleted")
                        st.rerun()
                else:
                    c.execute("DELETE FROM teams WHERE id=?", (team_id,))
                    conn.commit()
                    st.rerun()
        st.divider()
#------------------
#Matches hinzufügen
#------------------
        st.subheader(":material/Add_2: Add Match", anchor=False)
        teams = c.execute("SELECT id, name, class FROM teams").fetchall()
        team_dict = {name: tid for tid, name, klasse in teams}
        team_klasse = {name: klasse for tid, name, klasse in teams}
        names = list(team_dict.keys())

        with st.form("add_match", clear_on_submit=True, border=False):
            with st.container(horizontal=True,border=False, vertical_alignment="center",key="first"):
                p1_name = st.selectbox("Team 1", names,width=200,placeholder="Team 1",label_visibility="collapsed", index=None)
                p2_name = st.selectbox("Team 2", names,width=200,placeholder="Team 2",label_visibility="collapsed", index=None)
                stage_name = st.selectbox("Stage", ["Bracket","Quaters", "Semis", "Final", "Loser Final"], width=150,label_visibility="collapsed",placeholder="Stage", index=None)
                court = st.selectbox("Court", list(range(1,10)), width=100,placeholder="Court",label_visibility="collapsed", index=None)
                st.space("stretch")
                submit = st.form_submit_button(":material/Add_Circle:\u00A0\u00A0Add",width=100)
            if submit:                
                if team_klasse[p1_name]==team_klasse[p2_name]:
                    c.execute("""
                        INSERT INTO matches (player1_id, player2_id, court, is_visible, match_class, stage)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (team_dict[p1_name], team_dict[p2_name], court,0 ,team_klasse[p1_name], stage_name))
                    conn.commit()
                    st.rerun()
                else:
                    st.warning("Nicht in der gleichen Klasse.")
matches = c.execute("""
SELECT id, player1_id, player2_id, court, last_updated, is_visible, stage
FROM matches
""").fetchall()
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
    if not st.session_state.selected_match is None:
        if st.button(":material/undo: Back",width=100):
            st.session_state.selected_match = None
            st.rerun()
    if st.button(":material/refresh: Reload",width=100):
        st.rerun()
#------------------
#Spielliste
#------------------
if st.session_state.selected_match is None:
#------------------
#Spielliste für Nutzer
#------------------
    if st.session_state.language=="german":
        st.subheader("Laufende Spiele", anchor=False)
    else:
        st.subheader("Ongoing Matches", anchor=False)
    for m in matches:
        mid, p1, p2, court, updated, visible, match_stage = m
        if visible:    
            name1 = get_team_name(p1)
            name2 = get_team_name(p2)
            with st.container(horizontal=True):
                st.space("stretch")
                with st.container(horizontal=True,border=True, vertical_alignment="center",horizontal_alignment="center",width="content"):
                    if st.session_state.language=="german":
                        st.markdown(f"Auf Feld {court}:")
                    else:
                        st.markdown(f"On court {court}:")
                    if match_stage=="Quaters":
                        if st.session_state.language=="german":
                            st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#CD7F32"><u>Viertelfinale</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                        else:
                            st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#CD7F32"><u>Quater final</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                    elif match_stage=="Semis":
                        if st.session_state.language=="german":
                            st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#C0C0C0"><u>Halbfinale</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                        else:
                            st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#C0C0C0"><u>Semi final</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                    elif match_stage=="Final":
                        if st.session_state.language=="german":
                            st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#FFD700"><u>Finale</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                        else:
                            st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#FFD700"><u>Final</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                    elif match_stage=="Loser Final":
                        if st.session_state.language=="german":
                            st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#FFD700"><u>Spiel um Platz 3</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                        else:
                            st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#FFD700"><u>Game for 3rd place</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                    else:
                        st.markdown(f"""<div style="margin-top:-18px"><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                    if st.session_state.admin:
                        if st.button(":material/Edit_Square:", key=f"open_{mid}"):
                            st.session_state.selected_match = mid
                            st.rerun()
                    if st.session_state.admin and visible and not st.session_state.input_mode:
                        if st.button(":material/Visibility_Off:", key=f"vis_match_{mid}"):
                            c.execute("UPDATE matches SET is_visible=? WHERE id=?", (0,mid))
                            conn.commit()
                            st.rerun()
                    elif st.session_state.admin and not visible and not st.session_state.input_mode:
                        if st.button(":material/Visibility:", key=f"vis_match_{mid}"):
                            c.execute("UPDATE matches SET is_visible=? WHERE id=?", (1,mid))
                            conn.commit()
                            st.rerun()
                    if st.session_state.admin and not st.session_state.input_mode:
                        if st.button(":material/Delete:", key=f"del_match_{mid}"):
                            c.execute("DELETE FROM matches WHERE id=?", (mid,))
                            conn.commit()
                            st.success("Match deleted")
                            st.rerun()
                st.space("stretch")
#------------------
#Abgeschlossene Spiele für Admin
#------------------
    if st.session_state.admin and not st.session_state.input_mode:
        st.subheader("Ausgeblendete Matches", anchor=False)
        for m in matches:
            mid, p1, p2, court, updated, visible, match_stage = m
            if not visible:    
                name1 = get_team_name(p1)
                name2 = get_team_name(p2)
                with st.container(horizontal=True):
                    st.space("stretch")
                    with st.container(horizontal=True,border=True, vertical_alignment="center",horizontal_alignment="center",width="content",height=80):
                        if st.session_state.language=="german":
                            st.markdown(f"Auf Feld {court}:")
                        else:
                            st.markdown(f"On court {court}:")
                        if match_stage=="Quaters":
                            if st.session_state.language=="german":
                                st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#CD7F32"><u>Viertelfinale</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                            else:
                                st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#CD7F32"><u>Quater final</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                        elif match_stage=="Semis":
                            if st.session_state.language=="german":
                                st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#C0C0C0"><u>Halbfinale</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                            else:
                                st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#C0C0C0"><u>Semi final</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                        elif match_stage=="Final":
                            if st.session_state.language=="german":
                                st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#FFD700"><u>Finale</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                            else:
                                st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#FFD700"><u>Final</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                        elif match_stage=="Loser Final":
                            if st.session_state.language=="german":
                                st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#FFD700"><u>Spiel um Platz 3</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                            else:
                                st.markdown(f"""<div style="margin-top:-20px"><div style="text-align:center;"><span style="color:#FFD700"><u>Game for 3rd place</u></span></div><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                        else:
                            st.markdown(f"""<div style="margin-top:-18px"><div style="text-align:center;"><b>{name1}</b> vs <b>{name2}</b></div></div>""", width=350,unsafe_allow_html=True)
                        if st.session_state.admin:
                            if st.button(":material/Edit_Square:", key=f"open_{mid}"):
                                st.session_state.selected_match = mid
                                st.rerun()
                        if st.session_state.admin and visible and not st.session_state.input_mode:
                            if st.button(":material/Visibility_Off:", key=f"vis_match_{mid}"):
                                c.execute("UPDATE matches SET is_visible=? WHERE id=?", (0,mid))
                                conn.commit()
                                st.rerun()
                        elif st.session_state.admin and not visible and not st.session_state.input_mode:
                            if st.button(":material/Visibility:", key=f"vis_match_{mid}"):
                                c.execute("UPDATE matches SET is_visible=? WHERE id=?", (1,mid))
                                conn.commit()
                                st.rerun()
                        if st.session_state.admin and not st.session_state.input_mode:
                            if st.button(":material/Delete:", key=f"del_match_{mid}"):
                                c.execute("DELETE FROM matches WHERE id=?", (mid,))
                                conn.commit()
                                st.success("Match deleted")
                                st.rerun()
                    st.space("stretch")
#------------------
#Spielberichte
#------------------
else:
    mid = st.session_state.selected_match
    m = c.execute("""
    SELECT * FROM matches WHERE id=?
    """, (mid,)).fetchone()
    (_, p1, p2, court,
     s1p1, s1p2, s2p1, s2p2, s3p1, s3p2,
     last_updated, _, is_visible, klasse, stage_name) = m
    already_filled=False
    prev_s1p1=0
    prev_s1p2=0
    prev_s2p1=0
    prev_s2p2=0
    prev_s3p1=0
    prev_s3p2=0
    if not(s1p1 is None and s1p2 is None and s2p1 is None and s2p2 is None and s3p1 is None and s3p2 is None):
        already_filled=True
        prev_s1p1=s1p1
        prev_s1p2=s1p2
        prev_s2p1=s2p1
        prev_s2p2=s2p2
        prev_s3p1=s3p1
        prev_s3p2=s3p2
    name1 = get_team_name(p1)
    name2 = get_team_name(p2)
    st.subheader(f"***{name1}*** vs ***{name2}***",anchor=False)
    is_locked = last_updated is not None and not st.session_state.admin
    with st.container(horizontal=True):
        st.space("stretch")
        with st.form("result_form", width=700):
            with st.container(horizontal=True):
                # --- SET 1 ---
                with st.container():
                    with st.container(horizontal=True,width=300):
                        st.space("stretch")
                        if st.session_state.language=="german":
                            st.markdown("1. Satz",text_alignment="center")
                        else:
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
                        if st.session_state.language=="german":
                            st.markdown("2. Satz",text_alignment="center")
                        else:
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
                        if st.session_state.language=="german":
                            st.markdown("3. Satz",text_alignment="center")
                        else:
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
                sub_button_text=""
                if st.session_state.language=="german":
                    sub_button_text="Abgeben"
                else:
                    sub_button_text="Hand in"
                submit = st.form_submit_button(sub_button_text, disabled=is_locked,width=200)
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
            c.execute("UPDATE matches SET s1_p1=?, s1_p2=?, s2_p1=?, s2_p2=?, s3_p1=?, s3_p2=? WHERE id=?", (s1a, s1b, s2a, s2b, s3a_val, s3b_val, mid))
            conn.commit()
            winner_id = recompute_team_stats(mid, stage_name, prev_s1p1, prev_s1p2, prev_s2p1, prev_s2p2, prev_s3p1, prev_s3p2)
            settings= c.execute("SELECT id, group_number FROM settings WHERE class =?",(klasse,)).fetchall()
            if stage_name == 'Quaters':
                if settings[0][1]==4:
                    if c.execute("SELECT team_group, group_placement FROM teams WHERE id=?",(winner_id,)).fetchone():
                        winner = c.execute("SELECT team_group, group_placement FROM teams WHERE id=?",(winner_id,)).fetchone()
                    winner_group, winner_placement = winner
                    if winner_group=='A' and winner_placement ==1:
                        c.execute("UPDATE teams SET quaters_nr_winner=1 WHERE id=?",(winner_id,))
                    if winner_group=='A' and winner_placement ==2:
                        c.execute("UPDATE teams SET quaters_nr_winner=4 WHERE id=?",(winner_id,))
                    if winner_group=='B' and winner_placement ==1:
                        c.execute("UPDATE teams SET quaters_nr_winner=3 WHERE id=?",(winner_id,))
                    if winner_group=='B' and winner_placement ==2:
                        c.execute("UPDATE teams SET quaters_nr_winner=2 WHERE id=?",(winner_id,))
                    if winner_group=='C' and winner_placement ==1:
                        c.execute("UPDATE teams SET quaters_nr_winner=2 WHERE id=?",(winner_id,))
                    if winner_group=='C' and winner_placement ==2:
                        c.execute("UPDATE teams SET quaters_nr_winner=3 WHERE id=?",(winner_id,))
                    if winner_group=='D' and winner_placement ==1:
                        c.execute("UPDATE teams SET quaters_nr_winner=4 WHERE id=?",(winner_id,))
                    if winner_group=='D' and winner_placement ==2:
                        c.execute("UPDATE teams SET quaters_nr_winner=1 WHERE id=?",(winner_id,))
                    conn.commit()
                elif settings[0][1]==3:
                    if c.execute("SELECT id, name FROM teams WHERE class=? and group_placement=?",(klasse, 3)).fetchone():
                        S_teams = c.execute("SELECT id, name, team_group FROM teams WHERE class=? and group_placement=? ORDER BY wins DESC, lsets ASC, lpoints ASC",(klasse, 3)).fetchall()
                        is_done_list = c.execute("SELECT group_name FROM groups WHERE class=? and is_done=1",(klasse,)).fetchall()
                        if len(is_done_list)==3:
                            if S_teams[2][2]=='C':
                                c.execute("UPDATE settings SET which_third_is_missing=3 WHERE class=?",(klasse,))
                                conn.commit()
                                if (get_team_group(p1)=='A' and get_team_placement(p1)==1) or (get_team_group(p2)=='A' and get_team_placement(p2)==1):
                                    c.execute("UPDATE teams SET quaters_nr_winner=1 WHERE id=?",(winner_id,))
                                if (get_team_group(p1)=='B' and get_team_placement(p1)==1) or (get_team_group(p2)=='B' and get_team_placement(p2)==1):
                                    c.execute("UPDATE teams SET quaters_nr_winner=2 WHERE id=?",(winner_id,))
                                if (get_team_group(p1)=='C' and get_team_placement(p1)==1) or (get_team_group(p2)=='C' and get_team_placement(p2)==1):
                                    c.execute("UPDATE teams SET quaters_nr_winner=3 WHERE id=?",(winner_id,))
                                if (get_team_group(p1)=='A' and get_team_placement(p1)==2) or (get_team_group(p2)=='A' and get_team_placement(p2)==2):
                                    c.execute("UPDATE teams SET quaters_nr_winner=4 WHERE id=?",(winner_id,))
                                conn.commit()
                            if S_teams[2][2]=='B':
                                c.execute("UPDATE settings SET which_third_is_missing=2 WHERE class=?",(klasse,))
                                conn.commit()
                                if (get_team_group(p1)=='A' and get_team_placement(p1)==1) or (get_team_group(p2)=='A' and get_team_placement(p2)==1):
                                    c.execute("UPDATE teams SET quaters_nr_winner=1 WHERE id=?",(winner_id,))
                                if (get_team_group(p1)=='B' and get_team_placement(p1)==1) or (get_team_group(p2)=='B' and get_team_placement(p2)==1):
                                    c.execute("UPDATE teams SET quaters_nr_winner=3 WHERE id=?",(winner_id,))
                                if (get_team_group(p1)=='C' and get_team_placement(p1)==1) or (get_team_group(p2)=='C' and get_team_placement(p2)==1):
                                    c.execute("UPDATE teams SET quaters_nr_winner=2 WHERE id=?",(winner_id,))
                                if (get_team_group(p1)=='A' and get_team_placement(p1)==2) or (get_team_group(p2)=='A' and get_team_placement(p2)==2):
                                    c.execute("UPDATE teams SET quaters_nr_winner=4 WHERE id=?",(winner_id,))
                                conn.commit()
                            if S_teams[2][2]=='A':
                                c.execute("UPDATE settings SET which_third_is_missing=1 WHERE class=?",(klasse,))
                                conn.commit()
                                if (get_team_group(p1)=='A' and get_team_placement(p1)==1) or (get_team_group(p2)=='A' and get_team_placement(p2)==1):
                                    c.execute("UPDATE teams SET quaters_nr_winner=3 WHERE id=?",(winner_id,))
                                if (get_team_group(p1)=='B' and get_team_placement(p1)==1) or (get_team_group(p2)=='B' and get_team_placement(p2)==1):
                                    c.execute("UPDATE teams SET quaters_nr_winner=1 WHERE id=?",(winner_id,))
                                if (get_team_group(p1)=='C' and get_team_placement(p1)==1) or (get_team_group(p2)=='C' and get_team_placement(p2)==1):
                                    c.execute("UPDATE teams SET quaters_nr_winner=2 WHERE id=?",(winner_id,))
                                if (get_team_group(p1)=='A' and get_team_placement(p1)==2) or (get_team_group(p2)=='A' and get_team_placement(p2)==2):
                                    c.execute("UPDATE teams SET quaters_nr_winner=4 WHERE id=?",(winner_id,))
                                conn.commit()

            if stage_name == 'Semis':
                if c.execute("SELECT name, quaters_nr_winner FROM teams WHERE id=?",(winner_id,)).fetchone():
                    winner = c.execute("SELECT name, quaters_nr_winner FROM teams WHERE id=?",(winner_id,)).fetchone()
                winner_name, winner_quaters = winner
                if winner_quaters==1 or winner_quaters ==2:
                    c.execute("UPDATE teams SET semis_nr_winner=1 WHERE id=?",(winner_id,))
                    if winner_id==p1:
                        c.execute("UPDATE teams SET semis_nr_loser=1 WHERE id=?",(p2,))
                    else:
                        c.execute("UPDATE teams SET semis_nr_loser=1 WHERE id=?",(p1,))
                if winner_quaters==3 or winner_quaters ==4:
                    c.execute("UPDATE teams SET semis_nr_winner=2 WHERE id=?",(winner_id,))
                    if winner_id==p1:
                        c.execute("UPDATE teams SET semis_nr_loser=2 WHERE id=?",(p2,))
                    else:
                        c.execute("UPDATE teams SET semis_nr_loser=2 WHERE id=?",(p1,))
                conn.commit()
            if stage_name == 'Loser Final':
                c.execute("UPDATE teams SET third_place=1 WHERE id=?",(winner_id,))
                conn.commit()
            if stage_name=='Final':
                c.execute("UPDATE teams SET finals_winner=1 WHERE id=?",(winner_id,))
                conn.commit()
            st.rerun()
    with st.container(horizontal=True):
        st.space("stretch")
        if is_locked:
                st.warning("Ergebnisse abgegeben.",width=200)
        st.space("stretch")