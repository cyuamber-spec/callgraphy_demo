# -*- coding: utf-8 -*-
"""补充爬取脚本：修复未匹配和错误匹配的作品

针对首轮爬取中 7 个未匹配 + 2 个错误匹配的作品，使用不同的搜索关键词重试。
"""

import os
import re
import time
import sqlite3
import requests
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "static" / "images"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

DYNASTY_SHORT = {
    "秦": "秦", "东汉": "汉", "三国魏": "魏", "东晋": "晋",
    "唐": "唐", "北宋": "宋", "南宋": "宋", "元": "元",
    "明": "明", "清": "清", "近现代": "",
}

# 需要修复的作品：id -> (备选搜索关键词列表)
FIX_WORKS = {
    32: ["澄心堂纸", "澄心堂"],
    38: ["海棠诗 鲜于枢", "苏轼海棠诗", "海棠诗"],
    40: ["蜀道难 董其昌", "行书蜀道难"],
    44: ["难得糊涂", "难得糊涂 郑板桥"],
    45: ["竹石图 郑板桥", "竹石题跋", "竹石图题跋"],
    46: ["四条屏 何绍基", "何绍基行书", "何绍基"],
    48: ["篆书对联 吴昌硕", "吴昌硕篆书", "吴昌硕对联"],
    51: ["论书诗 林散之", "林散之草书", "林散之"],
    52: ["论书绝句 启功", "启功论书", "启功"],
}


def download_image(url, save_path):
    """下载图片到本地（带 Referer 防盗链）"""
    try:
        r = requests.get(
            url,
            headers={"Referer": "https://g2.ltfc.net/", "User-Agent": UA},
            timeout=30,
        )
        if r.status_code == 200 and len(r.content) > 1000:
            with open(save_path, "wb") as f:
                f.write(r.content)
            return True
        return False
    except Exception as e:
        print(f"    下载失败: {e}")
        return False


def extract_cards(page):
    """从搜索结果页 DOM 提取卡片：{title, meta, thumb}"""
    cards = page.evaluate(
        """() => {
          const imgs = [...document.querySelectorAll('img')].filter(im =>
            (im.src.includes('ltfc') || im.src.includes('quanku') || im.src.includes('cags'))
            && !im.src.includes('data:') && !im.src.includes('icon') && !im.src.includes('qrcode'));
          const results = [];
          const seen = new Set();
          for (const im of imgs) {
            if (seen.has(im.src)) continue;
            seen.add(im.src);
            let card = im;
            for (let i = 0; i < 6; i++) {
              if (card.parentElement) card = card.parentElement;
              const txt = (card.innerText || '').trim();
              if (txt.length > 2 && txt.length < 300) break;
            }
            let lines = (card.innerText || '').trim().split('\\n').map(t => t.trim()).filter(Boolean);
            lines = lines.filter(t => !/^(VIP|注|\\d+(\\.\\d+)?万?|\\d+)$/.test(t));
            if (lines.length === 0) continue;
            results.push({title: lines[0], meta: lines[1] || '', thumb: im.src});
          }
          return results;
        }"""
    )
    return cards


def match_card_strict(work_name, calligrapher, dynasty, cards):
    """严格匹配：要求作者名必须出现在 meta 中"""
    target_author = calligrapher
    target_dyn = DYNASTY_SHORT.get(dynasty, dynasty)
    best = None
    best_score = -1
    for c in cards:
        title = c["title"]
        meta = c["meta"]
        score = 0
        # 作者匹配（必须命中）
        if target_author and target_author in meta:
            score += 100
        else:
            continue  # 严格模式：作者不匹配直接跳过
        # 朝代匹配
        if target_dyn and target_dyn in meta:
            score += 30
        # 作品名匹配
        if title == work_name:
            score += 50
        elif title.startswith(work_name + "（") or title.startswith(work_name + "("):
            score += 45
        elif title.startswith(work_name):
            score += 35
        elif work_name in title:
            score += 15
        if score > best_score:
            best_score = score
            best = c
    if best_score >= 100:
        return best, best_score
    return None, best_score


def search_work(page, keyword):
    """搜索关键词并返回卡片列表"""
    if "search" not in page.url:
        page.goto("https://g2.ltfc.net/search_transit", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)
    search_input = page.query_selector("input[type=text]")
    if not search_input:
        page.goto("https://g2.ltfc.net/search_transit", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)
        search_input = page.query_selector("input[type=text]")
    search_input.fill("")
    page.wait_for_timeout(200)
    search_input.fill(keyword)
    page.wait_for_timeout(600)
    page.keyboard.press("Enter")
    page.wait_for_timeout(7000)
    for _ in range(3):
        page.mouse.wheel(0, 1800)
        page.wait_for_timeout(1500)
    return extract_cards(page)


def get_detail_large_image(page, card_thumb_url):
    """进入详情页，获取最大图片 URL"""
    clicked = False
    for im in page.query_selector_all("img"):
        src = im.get_attribute("src") or ""
        if card_thumb_url and card_thumb_url.split("?")[0] in src:
            try:
                im.click(timeout=5000)
                clicked = True
                break
            except Exception:
                pass
    if not clicked:
        return None
    page.wait_for_timeout(8000)
    big = page.evaluate(
        """() => {
          const imgs = [...document.querySelectorAll('img')].filter(im =>
            (im.src.includes('ltfc') || im.src.includes('quanku') || im.src.includes('cags'))
            && !im.src.includes('data:'));
          let best = null, bestW = 0;
          for (const im of imgs) {
            const w = im.naturalWidth || 0;
            if (w > bestW) { bestW = w; best = im.currentSrc || im.src; }
          }
          return {url: best, width: bestW};
        }"""
    )
    return big


def main():
    conn = sqlite3.connect(str(BASE_DIR / "calligraphy.db"))
    conn.row_factory = sqlite3.Row
    works = conn.execute(
        """SELECT w.id, w.name, c.name as calligrapher_name, d.name as dynasty_name
           FROM works w
           JOIN calligraphers c ON w.calligrapher_id = c.id
           JOIN dynasties d ON c.dynasty_id = d.id
           WHERE w.id IN (32, 38, 40, 44, 45, 46, 48, 51, 52)
           ORDER BY w.id"""
    ).fetchall()
    conn.close()

    fixed = []
    still_failed = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=UA, viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.goto("https://g2.ltfc.net/search_transit", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)

        for w in works:
            wid = w["id"]
            wname = w["name"]
            author = w["calligrapher_name"]
            dynasty = w["dynasty_name"]
            keywords = FIX_WORKS.get(wid, [wname])
            print(f"\n[id={wid}] 「{wname}」- {author} ({dynasty})")
            print(f"  尝试关键词: {keywords}")

            found = False
            for kw in keywords:
                print(f"  搜索: {kw}")
                try:
                    cards = search_work(page, kw)
                except Exception as e:
                    print(f"    搜索异常: {e}")
                    continue

                print(f"    获取到 {len(cards)} 张卡片")
                best, score = match_card_strict(wname, author, dynasty, cards)
                if not best:
                    print(f"    ✗ 严格匹配未命中（最高分 {score}）")
                    continue

                print(f"    ✓ 匹配: 「{best['title']}」/ {best['meta']} (score={score})")

                # 删除旧的错误图片（如有）
                for suffix in ["thumb", "large"]:
                    old = IMG_DIR / f"work_{wid}_{suffix}.jpg"
                    if old.exists():
                        old.unlink()

                # 下载缩略图
                thumb_path = IMG_DIR / f"work_{wid}_thumb.jpg"
                if download_image(best["thumb"], thumb_path):
                    print(f"    缩略图已保存: {thumb_path.name}")
                else:
                    print(f"    缩略图下载失败")
                    continue

                # 获取大图
                large_path = IMG_DIR / f"work_{wid}_large.jpg"
                try:
                    big = get_detail_large_image(page, best["thumb"])
                    if big and big.get("url"):
                        if download_image(big["url"], large_path):
                            print(f"    大图已保存 (宽{big['width']}px): {large_path.name}")
                        else:
                            shutil.copy(thumb_path, large_path)
                    else:
                        shutil.copy(thumb_path, large_path)
                except Exception as e:
                    print(f"    大图获取异常: {e}，用缩略图替代")
                    shutil.copy(thumb_path, large_path)

                fixed.append(wid)
                found = True
                time.sleep(1.5)
                break  # 匹配成功，不再尝试下一个关键词

            if not found:
                still_failed.append(wid)
                print(f"  ✗ 所有关键词均未匹配")

        browser.close()

    print("\n" + "=" * 50)
    print(f"补充爬取完成：修复 {len(fixed)} 件，仍失败 {len(still_failed)} 件")
    print(f"已修复: {fixed}")
    print(f"仍失败: {still_failed}")


if __name__ == "__main__":
    main()
