# -*- coding: utf-8 -*-
"""中华珍宝馆爬取侦察脚本 v4

默认 tab 即作品搜索。直接输入「兰亭序」回车，捕获作品搜索 API 及结果结构。
"""

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
            api_responses.append({"url": url, "status": response.status, "body": body[:5000]})

        page.on("response", on_response)

        print("=== 打开 search_transit（默认作品搜索tab）===")
        page.goto("https://g2.ltfc.net/search_transit", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)

        # input 0 是作品搜索框
        print("\n=== 输入「兰亭序」===")
        work_input = page.query_selector("input[type=text]")
        if work_input:
            ph = work_input.get_attribute("placeholder")
            print(f"  placeholder: {ph}")
            work_input.click()
            page.wait_for_timeout(300)
            work_input.fill("兰亭序")
            page.wait_for_timeout(800)
            page.keyboard.press("Enter")
            page.wait_for_timeout(10000)

        print(f"\n=== 当前 URL: {page.url} ===")

        # 打印所有 API 响应，重点看含 search 的
        print(f"\n=== 所有 API 响应（共 {len(api_responses)} 条）===")
        for i, r in enumerate(api_responses):
            url = r["url"]
            short = url.split("api.quanku.art/")[-1]
            print(f"\n--- [{i}] {r['status']} {short}")
            body = r["body"]
            # 重点打印含 兰亭/搜索结果/作品列表 的
            if "兰亭" in body or "search" in url.lower() or "Search" in url:
                print(body[:3000])
            else:
                print(body[:150])

        # 打印页面中的图片（搜索结果缩略图）
        print("\n=== 页面 img（结果缩略图）===")
        imgs = page.eval_on_selector_all(
            "img",
            """els => els.map(e => ({src: e.src, alt: e.alt}))
               .filter(x => x.src && !x.src.includes('data:') && (x.src.includes('ltfc') || x.src.includes('quanku')))""",
        )
        for im in imgs[:25]:
            print(f"  {im['alt'] or '(no alt)'} -> {im['src']}")

        # 打印页面链接（作品详情页 URL 规律）
        print("\n=== 页面链接 ===")
        links = page.eval_on_selector_all(
            "a",
            "els => els.map(e => ({href: e.href, text: e.innerText.trim().substring(0,25)})).filter(x => x.href && x.text && x.text.length>1)",
        )
        for l in links[:30]:
            print(f"  {l['text']} -> {l['href']}")

        page.screenshot(path="/tmp/ltfc_recon4.png", full_page=False)
        print("\n截图: /tmp/ltfc_recon4.png")
        browser.close()


if __name__ == "__main__":
    main()
