# -*- coding: utf-8 -*-
"""数据库初始化与连接管理

使用 SQLite 作为小型数据库，存储历代书法家及作品数据。
首次运行时自动建表并填充数据。
"""

import os
import sqlite3
from pathlib import Path

# 数据库文件路径
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "calligraphy.db"


def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # 返回字典形式
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """初始化数据库：建表并填充数据"""
    from data.calligraphers_data import DYNASTIES, CALLIGRAPHERS

    # 如已存在则先删除，确保数据最新
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = get_connection()
    cursor = conn.cursor()

    # 创建朝代表
    cursor.execute("""
        CREATE TABLE dynasties (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            sort_order INTEGER NOT NULL,
            start_year INTEGER,
            end_year INTEGER
        )
    """)

    # 创建书法家表
    cursor.execute("""
        CREATE TABLE calligraphers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dynasty_id INTEGER NOT NULL,
            birth_year INTEGER,
            death_year INTEGER,
            style TEXT,
            introduction TEXT,
            FOREIGN KEY (dynasty_id) REFERENCES dynasties(id)
        )
    """)

    # 创建作品表
    cursor.execute("""
        CREATE TABLE works (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            calligrapher_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            style TEXT,
            description TEXT,
            creation_year INTEGER,
            FOREIGN KEY (calligrapher_id) REFERENCES calligraphers(id)
        )
    """)

    # 创建索引以提升查询性能
    cursor.execute("CREATE INDEX idx_calligraphers_dynasty ON calligraphers(dynasty_id)")
    cursor.execute("CREATE INDEX idx_works_calligrapher ON works(calligrapher_id)")

    # 填充朝代数据
    for d in DYNASTIES:
        cursor.execute(
            "INSERT INTO dynasties (name, sort_order, start_year, end_year) VALUES (?, ?, ?, ?)",
            (d["name"], d["sort_order"], d["start_year"], d["end_year"]),
        )

    # 填充书法家及作品数据
    dynasty_map = {d["name"]: d["sort_order"] for d in DYNASTIES}

    for c in CALLIGRAPHERS:
        dynasty_id = dynasty_map.get(c["dynasty"])
        if dynasty_id is None:
            continue

        cursor.execute(
            """INSERT INTO calligraphers
               (name, dynasty_id, birth_year, death_year, style, introduction)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (c["name"], dynasty_id, c["birth_year"], c["death_year"],
             c["style"], c["introduction"]),
        )
        calligrapher_id = cursor.lastrowid

        for w in c.get("works", []):
            cursor.execute(
                """INSERT INTO works
                   (calligrapher_id, name, style, description, creation_year)
                   VALUES (?, ?, ?, ?, ?)""",
                (calligrapher_id, w["name"], w["style"],
                 w["description"], w.get("creation_year")),
            )

    conn.commit()
    conn.close()

    print(f"[数据库] 初始化完成：{DB_PATH}")
    print(f"  - 朝代：{len(DYNASTIES)} 个")
    print(f"  - 书法家：{len(CALLIGRAPHERS)} 位")
    total_works = sum(len(c.get("works", [])) for c in CALLIGRAPHERS)
    print(f"  - 作品：{total_works} 件")


if __name__ == "__main__":
    init_db()
