# -*- coding: utf-8 -*-
"""中华珍宝馆爬取侦察脚本 v2

在 search_transit 页面真实搜索「兰亭序」，捕获搜索 API 的请求与响应，
提取作品 objectId 及图片 URL 规律。
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

        api_responses = []

        def on_response(response):
            url = response.url
            if "api.quanku.art" not in url:
                return
            try:
                body = response.text()
            except Exception:
                body = ""
            api_responses.append({"url": url, "status": response.status, "body": body[:3000]})

        page.on("response", on_response)

        # 打开搜索页
        print("=== 打开 search_transit ===")
        page.goto(
            "https://g2.ltfc.net/search_transit?defaultTabKey=1",
            wait_until="domcontentloaded",
            timeout=60000,
        )
        page.wait_for_timeout(5000)

        # 找搜索框
        print("\n=== 查找搜索框 ===")
        for sel in [
            'input[placeholder*="搜索"]',
            'input[placeholder*="书法"]',
            'input[placeholder*="画"]',
            'input[type="search"]',
            'input[type="text"]',
            "input",
        ]:
            els = page.query_selector_all(sel)
            print(f"  selector={sel} -> {len(els)} 个")
            for e in els[:5]:
                try:
                    vis = e.is_visible()
                    ph = e.get_attribute("placeholder")
                    print(f"    visible={vis} placeholder={ph}")
                except Exception:
                    pass

        # 尝试输入
        search_input = None
        for sel in [
            'input[placeholder*="搜索"]',
            'input[placeholder*="书法"]',
            'input[type="text"]',
            "input",
        ]:
            els = page.query_selector_all(sel)
            for e in els:
                try:
                    if e.is_visible():
                        search_input = e
                        break
                except Exception:
                    pass
            if search_input:
                break

        if search_input:
            print("\n=== 输入「兰亭序」并搜索 ===")
            search_input.click()
            page.wait_for_timeout(500)
            search_input.fill("兰亭序")
            page.wait_for_timeout(1000)
            page.keyboard.press("Enter")
            page.wait_for_timeout(8000)
        else:
            print("未找到搜索框")

        print(f"\n=== 当前 URL: {page.url} ===")

        # 打印所有 API 响应
        print(f"\n=== API 响应（共 {len(api_responses)} 条）===")
        for i, r in enumerate(api_responses):
            print(f"\n--- [{i}] {r['status']} {r['url']}")
            # 只打印包含关键信息的响应
            body = r["body"]
            if "兰亭" in body or "thumb" in body or "picstore" in body or "name" in body:
                print(body[:2000])
            else:
                print(body[:200])

        page.screenshot(path="/tmp/ltfc_recon2.png", full_page=False)
        print("\n截图: /tmp/ltfc_recon2.png")

        browser.close()


if __name__ == "__main__":
    main()
