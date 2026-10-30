# -*- coding: utf-8 -*-
"""中华珍宝馆爬取侦察脚本 v5

搜索「兰亭序」后：
1. 从 DOM 提取结果卡片的「作品名 + 作者 + 朝代 + 缩略图URL」
2. 点击第一个书法结果，捕获作品详情 API（含完整图片URL）
3. 确定详情页 URL 规律与图片 URL 规律
"""

import re
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1440, "height": 900},
        )
        page = context.new_page()

        api_responses = []

        def on_response(response):
            url = response.url
            if "api.quanku.art" not in url:
                return
            try:
                body = response.text()
            except Exception:
                body = ""
            api_responses.append({"url": url, "status": response.status, "body": body})

        page.on("response", on_response)

        print("=== 搜索「兰亭序」===")
        page.goto("https://g2.ltfc.net/search_transit", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)
        work_input = page.query_selector("input[type=text]")
        work_input.click()
        page.wait_for_timeout(300)
        work_input.fill("兰亭序")
        page.wait_for_timeout(800)
        page.keyboard.press("Enter")
        page.wait_for_timeout(8000)

        # 滚动加载更多
        for _ in range(3):
            page.mouse.wheel(0, 1500)
            page.wait_for_timeout(2000)

        print(f"当前 URL: {page.url}")

        # 从 DOM 提取结果卡片：找所有含 ltfc/quanku 图片的元素，向上找卡片容器
        print("\n=== DOM 结果卡片（作品名/作者/朝代 + 缩略图）===")
        cards = page.evaluate(
            """() => {
              const imgs = [...document.querySelectorAll('img')].filter(im =>
                (im.src.includes('ltfc') || im.src.includes('quanku')) && !im.src.includes('data:'));
              const results = [];
              for (const im of imgs) {
                // 向上找卡片容器（含较多文字的祖先）
                let card = im;
                for (let i = 0; i < 5; i++) {
                  if (card.parentElement) card = card.parentElement;
                  const txt = (card.innerText || '').trim();
                  if (txt.length > 2 && txt.length < 200) break;
                }
                const txt = (card.innerText || '').trim().split('\\n').filter(t => t.trim());
                results.push({texts: txt.slice(0, 6), src: im.src});
              }
              return results;
            }"""
        )
        for i, c in enumerate(cards[:30]):
            print(f"\n  [{i}] img: {c['src'][:90]}")
            print(f"       文字: {c['texts']}")

        # 点击第一个结果，捕获详情 API
        print("\n\n=== 点击第一个结果查看详情 ===")
        first_img = None
        for im in page.query_selector_all("img"):
            src = im.get_attribute("src") or ""
            if ("ltfc" in src or "quanku" in src) and "data:" not in src:
                first_img = im
                break
        if first_img:
            # 向上找可点击卡片
            card = first_img
            for _ in range(5):
                if card.query_selector("a") or card.evaluate("el => el.onclick !== null"):
                    break
                if card.parentElement:
                    card = card.parentElement
            try:
                card.click(timeout=5000)
                page.wait_for_timeout(9000)
            except Exception as e:
                print(f"点击失败: {e}")

        print(f"详情页 URL: {page.url}")

        # 打印含图片URL的详情 API
        print("\n=== 详情相关 API（含 picstore/thumbstore/snapUrl/getById）===")
        for i, r in enumerate(api_responses):
            body = r["body"]
            if any(k in body for k in ["snapUrl", "picstore", "thumbTileUrl", "getById", "getDetail", "getSuha"]):
                short = r["url"].split("api.quanku.art/")[-1]
                print(f"\n--- [{i}] {r['status']} {short}")
                # 提取图片相关字段
                for key in ["snapUrl", "thumbTileUrl", "thumbTileUrlx2", "name", "author", "age", "Id", "picstore"]:
                    m = re.search(r'"%s"\s*:\s*"([^"]{0,200})' % key, body)
                    if m:
                        print(f"    {key}: {m.group(1)}")

        page.screenshot(path="/tmp/ltfc_recon5.png", full_page=False)
        browser.close()


if __name__ == "__main__":
    main()
