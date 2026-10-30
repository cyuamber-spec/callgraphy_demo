# -*- coding: utf-8 -*-
"""导出静态数据脚本

将后端 SQLite 中的数据导出为静态 JSON 文件，并将爬取的真实图片复制到前端 public 目录，
为没有真实图片的作品生成 SVG 占位图。用于 GitHub Pages 纯前端部署。

输出目录：
  frontend/public/data/   — 所有 API 响应的 JSON 快照
  frontend/public/images/ — 作品图片（真实 jpg + 占位 svg）
"""

import json
import shutil
from pathlib import Path

from database import get_connection
from image_generator import generate_work_svg

# 路径
BACKEND_DIR = Path(__file__).resolve().parent
FRONTEND_PUBLIC = BACKEND_DIR.parent / "frontend" / "public"
DATA_DIR = FRONTEND_PUBLIC / "data"
IMG_DIR = FRONTEND_PUBLIC / "images"
SRC_IMG_DIR = BACKEND_DIR / "static" / "images"

# 没有真实图片的作品 ID（回退到 SVG 占位）
NO_IMAGE_IDS = {32, 38, 40, 44, 45, 51}


def ensure_dirs():
    """创建输出目录"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[目录] data -> {DATA_DIR}")
    print(f"[目录] images -> {IMG_DIR}")


def dump_json(filename, data):
    """写入 JSON 文件"""
    path = DATA_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  [JSON] {filename} ({len(data) if isinstance(data, list) else 'obj'})")


def export_dynasties():
    """导出朝代列表"""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM dynasties ORDER BY sort_order").fetchall()
    conn.close()
    dump_json("dynasties.json", [dict(r) for r in rows])


def export_calligraphers():
    """导出书法家列表 + 每位书法家详情（含作品）"""
    conn = get_connection()
    rows = conn.execute(
        """SELECT c.*, d.name as dynasty_name, d.sort_order as dynasty_order
           FROM calligraphers c
           JOIN dynasties d ON c.dynasty_id = d.id
           ORDER BY d.sort_order, c.birth_year"""
    ).fetchall()
    conn.close()
    calligraphers = [dict(r) for r in rows]
    dump_json("calligraphers.json", calligraphers)

    # 每位书法家详情（含作品列表）
    conn = get_connection()
    for c in calligraphers:
        cid = c["id"]
        works = conn.execute(
            "SELECT * FROM works WHERE calligrapher_id = ? ORDER BY creation_year",
            (cid,),
        ).fetchall()
        detail = dict(c)
        detail["works"] = [dict(w) for w in works]
        dump_json(f"calligrapher_{cid}.json", detail)
    conn.close()


def export_works():
    """导出作品列表 + 每件作品详情"""
    conn = get_connection()
    rows = conn.execute(
        """SELECT w.*, c.name as calligrapher_name, c.style as calligrapher_style,
                  d.name as dynasty_name, d.sort_order as dynasty_order
           FROM works w
           JOIN calligraphers c ON w.calligrapher_id = c.id
           JOIN dynasties d ON c.dynasty_id = d.id
           ORDER BY d.sort_order, w.creation_year, c.birth_year"""
    ).fetchall()
    conn.close()
    works = [dict(r) for r in rows]
    dump_json("works.json", works)

    # 每件作品详情
    conn = get_connection()
    for w in works:
        wid = w["id"]
        work = conn.execute(
            """SELECT w.*, c.name as calligrapher_name, c.style as calligrapher_style,
                      c.id as calligrapher_id, d.name as dynasty_name
               FROM works w
               JOIN calligraphers c ON w.calligrapher_id = c.id
               JOIN dynasties d ON c.dynasty_id = d.id
               WHERE w.id = ?""",
            (wid,),
        ).fetchone()
        dump_json(f"work_{wid}.json", dict(work))
    conn.close()


def export_styles():
    """导出书体风格列表"""
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
    dump_json("styles.json", sorted(styles))


def export_stats():
    """导出统计数据"""
    conn = get_connection()
    data = {
        "dynasties": conn.execute("SELECT COUNT(*) as c FROM dynasties").fetchone()["c"],
        "calligraphers": conn.execute("SELECT COUNT(*) as c FROM calligraphers").fetchone()["c"],
        "works": conn.execute("SELECT COUNT(*) as c FROM works").fetchone()["c"],
    }
    conn.close()
    dump_json("stats.json", data)


def copy_images():
    """复制真实图片到前端 public/images/"""
    if not SRC_IMG_DIR.exists():
        print(f"  [警告] 源图片目录不存在: {SRC_IMG_DIR}")
        return
    count = 0
    for f in SRC_IMG_DIR.iterdir():
        if f.is_file() and f.suffix in (".jpg", ".jpeg"):
            shutil.copy2(f, IMG_DIR / f.name)
            count += 1
    print(f"  [图片] 复制 {count} 个真实图片文件")


def generate_svg_placeholders():
    """为没有真实图片的作品生成 SVG 占位图"""
    conn = get_connection()
    for wid in NO_IMAGE_IDS:
        work = conn.execute(
            """SELECT w.*, c.name as calligrapher_name, d.name as dynasty_name
               FROM works w
               JOIN calligraphers c ON w.calligrapher_id = c.id
               JOIN dynasties d ON c.dynasty_id = d.id
               WHERE w.id = ?""",
            (wid,),
        ).fetchone()
        if work is None:
            print(f"  [警告] 作品 id={wid} 不存在，跳过 SVG 生成")
            continue
        work_dict = dict(work)
        for size in ("thumbnail", "large"):
            suffix = "thumb" if size == "thumbnail" else "large"
            svg = generate_work_svg(work_dict, size=size)
            out = IMG_DIR / f"work_{wid}_{suffix}.svg"
            out.write_text(svg, encoding="utf-8")
        print(f"  [SVG] 作品 id={wid} {work_dict['name']} 占位图已生成")
    conn.close()


def main():
    print("=" * 50)
    print("导出静态数据用于 GitHub Pages 部署")
    print("=" * 50)
    ensure_dirs()
    print("\n[1/6] 导出朝代...")
    export_dynasties()
    print("\n[2/6] 导出书法家...")
    export_calligraphers()
    print("\n[3/6] 导出作品...")
    export_works()
    print("\n[4/6] 导出书体风格...")
    export_styles()
    print("\n[5/6] 导出统计...")
    export_stats()
    print("\n[6/6] 复制图片 & 生成 SVG 占位...")
    copy_images()
    generate_svg_placeholders()
    print("\n" + "=" * 50)
    print("导出完成！")
    print(f"  JSON 文件: {len(list(DATA_DIR.glob('*.json')))} 个")
    print(f"  图片文件: {len(list(IMG_DIR.iterdir()))} 个")
    print("=" * 50)


if __name__ == "__main__":
    main()
