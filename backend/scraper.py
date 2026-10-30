# -*- coding: utf-8 -*-
"""中华珍宝馆作品图批量爬取脚本

对数据库中每件作品：
1. 在中华珍宝馆搜索作品名
2. 从搜索结果 DOM 提取「作品名 + 朝代作者 + 缩略图URL」卡片
3. 用作者名 + 朝代做智能匹配，选出最佳结果
4. 下载缩略图到 backend/static/images/work_{id}_thumb.jpg
5. 点击匹配卡片进入详情页，提取页面中最大图片作为大图
6. 下载大图到 backend/static/images/work_{id}_large.jpg

匹配不到的作品会记录下来，最后输出报告。
图片带 auth_key 时效签名，故爬取后立即下载到本地，不再依赖外链。
"""

import os
import re
import time
import sqlite3
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "static" / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# 朝代简称映射（中华珍宝馆卡片用简称，如"晋 王羲之"）
DYNASTY_SHORT = {
    "秦": "秦", "东汉": "汉", "三国魏": "魏", "东晋": "晋",
    "唐": "唐", "北宋": "宋", "南宋": "宋", "元": "元",
    "明": "明", "清": "清", "近现代": "",
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
            // 过滤干扰词
            lines = lines.filter(t => !/^(VIP|注|\\d+(\\.\\d+)?万?|\\d+)$/.test(t));
            if (lines.length === 0) continue;
            results.push({title: lines[0], meta: lines[1] || '', thumb: im.src});
          }
          return results;
        }"""
    )
    return cards


def match_card(work_name, calligrapher, dynasty, cards):
    """智能匹配最佳卡片"""
    target_author = calligrapher
    target_dyn = DYNASTY_SHORT.get(dynasty, dynasty)
    best = None
    best_score = -1
    for c in cards:
        title = c["title"]
        meta = c["meta"]
        score = 0
        # 作者匹配（权重最高）
        if target_author and target_author in meta:
            score += 100
        # 朝代匹配
        if target_dyn and target_dyn in meta:
            score += 30
        # 作品名匹配
        if title == work_name:
            score += 50
        elif title.startswith(work_name + "（") or title.startswith(work_name + "("):
            score += 45  # 兰亭序（神龙本）匹配 兰亭序
        elif title.startswith(work_name):
            score += 35
        elif work_name in title:
            score += 15
        # 排除明显是当代人（meta 里只有名字无朝代，且浏览量极小）—— 靠作者匹配已能过滤
        if score > best_score:
            best_score = score
            best = c
    # 至少作者要匹配上
    if best_score >= 100:
        return best, best_score
    # 降级：无作者匹配但作品名完全一致
    if best_score >= 50:
        return best, best_score
    return None, best_score


def search_work(page, keyword):
    """搜索关键词并返回卡片列表"""
    # 确保在搜索页
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
    # 滚动加载更多
    for _ in range(3):
        page.mouse.wheel(0, 1800)
        page.wait_for_timeout(1500)
    return extract_cards(page)


def get_detail_large_image(page, card_thumb_url):
    """进入详情页，获取最大图片 URL。

    若详情页拿不到更大图，则回退使用缩略图。
    """
    # 点击第一个含缩略图的卡片
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

    # 详情页：找最大 naturalWidth 的 img
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
           ORDER BY w.id"""
    ).fetchall()
    conn.close()

    results = {"success": [], "no_match": [], "download_fail": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=UA, viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.goto("https://g2.ltfc.net/search_transit", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)

        for idx, w in enumerate(works):
            wid = w["id"]
            wname = w["name"]
            author = w["calligrapher_name"]
            dynasty = w["dynasty_name"]
            print(f"\n[{idx+1}/{len(works)}] id={wid} 「{wname}」- {author} ({dynasty})")

            try:
                cards = search_work(page, wname)
            except Exception as e:
                print(f"  搜索异常: {e}")
                results["no_match"].append(wid)
                continue

            print(f"  获取到 {len(cards)} 张卡片")
            best, score = match_card(wname, author, dynasty, cards)
            if not best:
                print(f"  ✗ 未匹配到（最高分 {score}）")
                results["no_match"].append(wid)
                continue

            print(f"  ✓ 匹配: 「{best['title']}」/ {best['meta']} (score={score})")

            # 下载缩略图
            thumb_path = IMG_DIR / f"work_{wid}_thumb.jpg"
            if download_image(best["thumb"], thumb_path):
                print(f"  缩略图已保存: {thumb_path.name}")
            else:
                print(f"  缩略图下载失败")
                results["download_fail"].append(wid)
                continue

            # 尝试获取详情页大图
            large_path = IMG_DIR / f"work_{wid}_large.jpg"
            try:
                big = get_detail_large_image(page, best["thumb"])
                if big and big.get("url"):
                    if download_image(big["url"], large_path):
                        print(f"  大图已保存 (宽{big['width']}px): {large_path.name}")
                    else:
                        print(f"  大图下载失败，用缩略图替代")
                        # 复制缩略图作为大图兜底
                        import shutil
                        shutil.copy(thumb_path, large_path)
                else:
                    print(f"  未获取到大图URL，用缩略图替代")
                    import shutil
                    shutil.copy(thumb_path, large_path)
            except Exception as e:
                print(f"  获取大图异常: {e}，用缩略图替代")
                import shutil
                shutil.copy(thumb_path, large_path)

            results["success"].append(wid)
            time.sleep(1.5)  # 礼貌延时

        browser.close()

    # 报告
    print("\n" + "=" * 50)
    print(f"爬取完成：成功 {len(results['success'])} / {len(works)}")
    print(f"未匹配: {results['no_match']}")
    print(f"下载失败: {results['download_fail']}")
    # 保存报告
    with open(BASE_DIR / "scrape_report.json", "w") as f:
        import json
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
