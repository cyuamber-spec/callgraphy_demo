# -*- coding: utf-8 -*-
"""书法作品集 - 后端 API 服务

基于 Flask 提供 RESTful API，前端通过这些接口获取朝代、书法家及作品数据。
"""

import os
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS
from database import get_connection, init_db
from image_generator import generate_work_svg

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)  # 允许前端跨域访问


# ============ API 接口 ============

@app.route("/api/health", methods=["GET"])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "service": "calligraphy-api"})


@app.route("/api/dynasties", methods=["GET"])
def get_dynasties():
    """获取所有朝代（按时间排序）"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM dynasties ORDER BY sort_order"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/calligraphers", methods=["GET"])
def get_calligraphers():
    """获取书法家列表

    支持按朝代筛选（dynasty 参数为朝代名称），默认按朝代排序、再按出生年排序。
    返回每位书法家的朝代名称。
    """
    dynasty = request.args.get("dynasty")

    conn = get_connection()
    if dynasty:
        rows = conn.execute(
            """SELECT c.*, d.name as dynasty_name, d.sort_order as dynasty_order
               FROM calligraphers c
               JOIN dynasties d ON c.dynasty_id = d.id
               WHERE d.name = ?
               ORDER BY d.sort_order, c.birth_year""",
            (dynasty,),
        ).fetchall()
    else:
        rows = conn.execute(
            """SELECT c.*, d.name as dynasty_name, d.sort_order as dynasty_order
               FROM calligraphers c
               JOIN dynasties d ON c.dynasty_id = d.id
               ORDER BY d.sort_order, c.birth_year"""
        ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/calligraphers/<int:cid>", methods=["GET"])
def get_calligrapher_detail(cid):
    """获取单个书法家详情及其作品列表"""
    conn = get_connection()
    calligrapher = conn.execute(
        """SELECT c.*, d.name as dynasty_name, d.sort_order as dynasty_order
           FROM calligraphers c
           JOIN dynasties d ON c.dynasty_id = d.id
           WHERE c.id = ?""",
        (cid,),
    ).fetchone()

    if calligrapher is None:
        conn.close()
        return jsonify({"error": "书法家不存在"}), 404

    works = conn.execute(
        """SELECT * FROM works WHERE calligrapher_id = ?
           ORDER BY creation_year""",
        (cid,),
    ).fetchall()
    conn.close()

    result = dict(calligrapher)
    result["works"] = [dict(w) for w in works]
    return jsonify(result)


@app.route("/api/works", methods=["GET"])
def get_works():
    """获取所有作品（按年代排序）

    支持按朝代（dynasty）和书体风格（style）筛选。
    返回作品连同其所属书法家与朝代信息。
    """
    dynasty = request.args.get("dynasty")
    style = request.args.get("style")

    query = """
        SELECT w.*, c.name as calligrapher_name, c.style as calligrapher_style,
               d.name as dynasty_name, d.sort_order as dynasty_order
        FROM works w
        JOIN calligraphers c ON w.calligrapher_id = c.id
        JOIN dynasties d ON c.dynasty_id = d.id
        WHERE 1=1
    """
    params = []
    if dynasty:
        query += " AND d.name = ?"
        params.append(dynasty)
    if style:
        query += " AND w.style = ?"
        params.append(style)
    query += " ORDER BY d.sort_order, w.creation_year, c.birth_year"

    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/works/<int:wid>", methods=["GET"])
def get_work_detail(wid):
    """获取单个作品详情"""
    conn = get_connection()
    work = conn.execute(
        """SELECT w.*, c.name as calligrapher_name, c.style as calligrapher_style,
                  c.id as calligrapher_id, d.name as dynasty_name
           FROM works w
           JOIN calligraphers c ON w.calligrapher_id = c.id
           JOIN dynasties d ON c.dynasty_id = d.id
           WHERE w.id = ?""",
        (wid,),
    ).fetchone()
    conn.close()

    if work is None:
        return jsonify({"error": "作品不存在"}), 404
    return jsonify(dict(work))


@app.route("/api/works/<int:wid>/image", methods=["GET"])
def get_work_image(wid):
    """获取作品图片

    优先返回从中华珍宝馆爬取的真实图片，找不到时回退到 SVG 生成。
    根据 size 参数返回缩略图或高清大图：
      - size=thumbnail  列表缩略图
      - size=large       详情高清大图
    """
    size = request.args.get("size", "large")
    if size not in ("thumbnail", "large"):
        size = "large"

    # 优先返回本地爬取的真实图片
    # 文件名约定：work_{id}_thumb.jpg（缩略图）、work_{id}_large.jpg（大图）
    img_dir = Path(__file__).resolve().parent / "static" / "images"
    file_suffix = "thumb" if size == "thumbnail" else "large"
    img_path = img_dir / f"work_{wid}_{file_suffix}.jpg"
    if img_path.exists():
        return send_from_directory(str(img_dir), img_path.name, mimetype="image/jpeg")

    # 回退：SVG 生成
    conn = get_connection()
    work = conn.execute(
        """SELECT w.*, c.name as calligrapher_name, d.name as dynasty_name
           FROM works w
           JOIN calligraphers c ON w.calligrapher_id = c.id
           JOIN dynasties d ON c.dynasty_id = d.id
           WHERE w.id = ?""",
        (wid,),
    ).fetchone()
    conn.close()

    if work is None:
        return jsonify({"error": "作品不存在"}), 404

    svg = generate_work_svg(dict(work), size=size)
    return Response(svg, mimetype="image/svg+xml")


@app.route("/api/styles", methods=["GET"])
def get_styles():
    """获取所有书体风格列表（用于筛选）"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT DISTINCT style FROM calligraphers WHERE style IS NOT NULL ORDER BY style"
    ).fetchall()
    work_styles = conn.execute(
        "SELECT DISTINCT style FROM works WHERE style IS NOT NULL ORDER BY style"
    ).fetchall()
    conn.close()

    styles = set()
    for r in rows:
        if r["style"]:
            styles.add(r["style"])
    for r in work_styles:
        if r["style"]:
            styles.add(r["style"])
    return jsonify(sorted(styles))


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """获取统计数据：朝代数、书法家家数、作品数"""
    conn = get_connection()
    dynasty_count = conn.execute("SELECT COUNT(*) as c FROM dynasties").fetchone()["c"]
    calligrapher_count = conn.execute("SELECT COUNT(*) as c FROM calligraphers").fetchone()["c"]
    work_count = conn.execute("SELECT COUNT(*) as c FROM works").fetchone()["c"]
    conn.close()
    return jsonify({
        "dynasties": dynasty_count,
        "calligraphers": calligrapher_count,
        "works": work_count,
    })


if __name__ == "__main__":
    # 首次运行初始化数据库
    if not (Path(__file__).resolve().parent / "calligraphy.db").exists():
        print("[启动] 首次运行，正在初始化数据库...")
        init_db()

    port = int(os.environ.get("PORT", 5001))
    print(f"[启动] 后端服务运行于 http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
