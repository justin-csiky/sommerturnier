"""Shared SQLite access and schema initialization for the tournament app.

The database file lives next to Home.py by default. Set TOURNEY_DB_PATH to
override the location (useful for local testing and deployment).
"""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("TOURNEY_DB_PATH", PROJECT_DIR / "data.db"))


def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection configured for concurrent app sessions."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.execute("PRAGMA busy_timeout = 10000")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    """Create the application's tables and insert missing default settings.

    Existing tournament data and existing settings are deliberately preserved.
    """
    connection = get_connection()
    try:
        # WAL allows readers to continue while another session writes.
        connection.execute("PRAGMA journal_mode = WAL")

        with connection:
            connection.execute(
                """
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
                """
            )
            connection.execute(
                """
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
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class TEXT,
                    group_name TEXT,
                    is_done INTEGER DEFAULT 0
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class TEXT,
                    group_number INTEGER DEFAULT 4,
                    which_third_is_missing INTEGER DEFAULT 0
                )
                """
            )

            # Add missing defaults without deleting or resetting existing settings.
            default_classes = ("LVL1/2", "MX", "DD", "HD")
            existing_classes = {
                row[0]
                for row in connection.execute(
                    "SELECT DISTINCT class FROM settings"
                ).fetchall()
            }
            for tournament_class in default_classes:
                if tournament_class not in existing_classes:
                    connection.execute(
                        "INSERT INTO settings (class) VALUES (?)",
                        (tournament_class,),
                    )
    finally:
        connection.close()
