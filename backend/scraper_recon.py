# -*- coding: utf-8 -*-
"""中华珍宝馆爬取侦察脚本

目标：打开网站，搜索「兰亭序」，拦截网络请求，找出搜索 API 端点
及图片 URL 规律，为批量爬取做准备。
"""

import json
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

        xhr_logs = []

        def on_request(request):
            rt = request.resource_type
            if rt in ("xhr", "fetch", "image"):
                xhr_logs.append({
                    "type": rt,
                    "method": request.method,
                    "url": request.url,
                    "post_data": (request.post_data or "")[:500],
                })

        page.on("request", on_request)

        # 1. 打开首页
        print("=== 打开首页 ===")
        page.goto("https://g2.ltfc.net/", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)

        # 打印所有 input
        inputs = page.eval_on_selector_all(
            "input",
            "els => els.map(e => ({tag: e.tagName, type: e.type, placeholder: e.placeholder, aria: e.getAttribute('aria-label'), class: e.className}))",
        )
        print("\n=== 页面 input 元素 ===")
        for i in inputs[:15]:
            print(" ", i)

        # 2. 尝试搜索「兰亭序」
        print("\n=== 尝试搜索 ===")
        # 优先找 placeholder 含"搜索"的 input
        search_input = None
        for sel in [
            'input[placeholder*="搜索"]',
            'input[placeholder*="书法"]',
            'input[type="search"]',
            'input[type="text"]',
        ]:
            try:
                el = page.query_selector(sel)
                if el and el.is_visible():
                    search_input = el
                    print(f"找到搜索框: selector={sel}")
                    break
            except Exception:
                continue

        if search_input:
            search_input.click()
            search_input.fill("兰亭序")
            page.wait_for_timeout(800)
            page.keyboard.press("Enter")
            page.wait_for_timeout(6000)
        else:
            print("未找到搜索框，尝试直接访问搜索结果页")
            page.goto(
                "https://g2.ltfc.net/search_transit?keyword=%E5%85%B0%E4%BA%AD%E5%BA%8F",
                wait_until="domcontentloaded",
                timeout=60000,
            )
            page.wait_for_timeout(6000)

        print(f"\n=== 当前 URL: {page.url} ===")

        # 3. 打印 xhr/fetch 请求（找 API）
        print("\n=== XHR/Fetch 请求（关键）===")
        for r in xhr_logs:
            if r["type"] in ("xhr", "fetch"):
                print(f"  [{r['method']}] {r['url']}")
                if r["post_data"]:
                    print(f"      post: {r['post_data']}")

        # 4. 打印图片请求（找 CDN 规律）
        print("\n=== 图片请求 ===")
        seen = set()
        for r in xhr_logs:
            if r["type"] == "image" and r["url"] not in seen:
                seen.add(r["url"])
                print(f"  {r['url']}")

        # 5. 打印页面中的链接（找作品详情页 URL 规律）
        links = page.eval_on_selector_all(
            "a",
            "els => els.map(e => ({href: e.href, text: e.innerText.trim().substring(0,30)})).filter(x => x.href && x.text)",
        )
        print("\n=== 页面链接（含文本）===")
        for l in links[:30]:
            print(f"  {l['text']} -> {l['href']}")

        # 6. 打印页面中的 img src
        imgs = page.eval_on_selector_all(
            "img",
            "els => els.map(e => ({src: e.src, alt: e.alt})).filter(x => x.src && !x.src.includes('data:'))",
        )
        print("\n=== 页面 img 标签 ===")
        for im in imgs[:20]:
            print(f"  {im['alt'] or '(no alt)'} -> {im['src']}")

        page.screenshot(path="/tmp/ltfc_recon.png", full_page=False)
        print("\n截图已保存: /tmp/ltfc_recon.png")

        browser.close()


if __name__ == "__main__":
    main()
