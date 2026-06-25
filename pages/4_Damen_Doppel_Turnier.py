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
    for i in r:
        if i[5]==group:
            table1.append([i[0],i[1],i[2],f"{i[3]} : {i[4]}"])
    if table1==[]:
        with st.container(horizontal=True):
            st.space("stretch")
            st.markdown(":blue[Turnierleitung erstellt Gruppe...]")
            st.space("stretch")
    else:
        rows_html = ""
        for name, wins, losses, diff in table1:
            rows_html += f'''<div class="row">
                    <div class="team">{name}</div>
                    <div class="stat">{wins}</div>
                    <div class="stat">{losses}</div>
                    <div class="stat">{diff}</div></div>'''
        st.markdown(f"""
            <style>
            .scroll-table {{
                overflow-x: auto;
                width: 100%;
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
                        <div class="team" style="color:#1c83e1;">Team Name</div>
                        <div class="stat"style="color:#21c354;">W</div>
                        <div class="stat"style="color:#ff4b4b;">L</div>
                        <div class="stat" style="color:#1c83e1;">+/-</div>
                    </div>
                    {rows_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
def finish_group(gname):
    groupid = c.execute("SELECT id, class FROM groups WHERE class=? and group_name=?", ('DD',gname)).fetchone()
    c.execute("UPDATE groups SET is_done=1 WHERE id=?",(groupid[0],))
    conn.commit()
    teams = c.execute("SELECT id FROM teams WHERE class=? and team_group=? ORDER BY wins DESC, lsets ASC, lpoints ASC", ('DD',gname)).fetchall()
    placement = 1
    for i in teams:
        id = i[0]
        c.execute("UPDATE teams SET group_placement=? WHERE id=?",(placement,id))
        placement+=1
    conn.commit()
    st.rerun()
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
if st.session_state.language=="german":
    st.subheader("Damen Doppel", anchor=False)
elif st.session_state.language=="english":
    st.subheader("Women's double", anchor=False)
settings= c.execute("SELECT id, group_number FROM settings WHERE class =?",('DD',)).fetchall()
if st.session_state.admin and not st.session_state.input_mode:
    if st.session_state.language=="german":
        tab1,tab2=st.tabs(["Gruppenphase","Einstellungen"])
    elif st.session_state.language=="english":
        tab1,tab2=st.tabs(["Group stage","Settings"])
    with tab1:
        with st.container(horizontal=True):
            st.space("stretch")
            with st.container(width=500):
                st.space("small")
                if st.session_state.language=="german":
                    grA = st.expander("Gruppe A", on_change="rerun",key="ad_gruppeA",expanded=True)
                elif st.session_state.language=="english":
                    grA = st.expander("Group A", on_change="rerun",key="ad_gruppeA",expanded=True)
                with grA:
                    raw = c.execute("""
                    SELECT name, wins, loses, wsets, lsets, team_group
                    FROM teams WHERE class=?
                    ORDER BY wins DESC, lsets ASC, lpoints ASC
                    """,('DD',)).fetchall()
                    print_table_alt(raw,'A')
                    st.space("xsmall")
                    with st.container(horizontal=True):
                        st.space("stretch")
                        if c.execute("SELECT id, class FROM groups WHERE is_done=0 and class='DD' and group_name='A'").fetchone():
                            if st.button(":red[Gruppe beenden]",width=200,key="ad_bt_gruppeA"):
                                finish_group('A')
                        else:
                            if st.button(":red[Platzierung neu eintragen]",width=200,key="ad_bt2_gruppeA"):
                                finish_group('A')
                        st.space("stretch")
            st.space("stretch")
    with tab2:
        if settings[0][1]==4:
            if st.checkbox("5er Gruppen"):         
                c.execute("UPDATE settings SET group_number=3 WHERE class=?",('DD',))
                conn.commit()
                st.rerun()
        if settings[0][1]==3:
            if st.checkbox("4er Gruppen"):         
                c.execute("UPDATE settings SET group_number=4 WHERE class=?",('DD',))
                c.execute("UPDATE settings SET which_third_is_missing=0 WHERE class=?",('DD',))
                conn.commit()
                st.rerun()
else:
    if st.session_state.language=="german":
        tab1= st.tabs(["Gruppenphase"])
    elif st.session_state.language=="english":
        tab1= st.tabs(["Group stage"])
    with tab1[0]:
        with st.container(horizontal=True):
            st.space("stretch")
            with st.container(width=600):
                st.space("small")
                if st.session_state.language=="german":
                    grA = st.expander("Gruppe A", on_change="rerun",key="ad_gruppeA",expanded=True)
                elif st.session_state.language=="english":
                    grA = st.expander("Group A", on_change="rerun",key="ad_gruppeA",expanded=True)
                with grA:
                    raw = c.execute("""
                    SELECT name, wins, loses, wsets, lsets, team_group
                    FROM teams WHERE class LIKE '%DD%'
                    ORDER BY wins DESC, lsets ASC, lpoints ASC
                    """).fetchall()
                    print_table_alt(raw,'A')
            st.space("stretch")