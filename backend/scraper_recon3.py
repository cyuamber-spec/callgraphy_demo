# -*- coding: utf-8 -*-
"""中华珍宝馆爬取侦察脚本 v3

切换到「作品搜索」tab，搜索「兰亭序」，捕获正确的作品搜索 API。
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
            if "/search" not in url and "Search" not in url:
                return
            try:
                body = response.text()
            except Exception:
                body = ""
            api_responses.append({"url": url, "status": response.status, "body": body[:4000]})

        page.on("response", on_response)

        print("=== 打开 search_transit（默认tab）===")
        page.goto("https://g2.ltfc.net/search_transit", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(5000)

        # 列出所有 input 及可见性
        print("\n=== 所有 input ===")
        inputs = page.eval_on_selector_all(
            "input",
            "els => els.map((e,i) => ({i, type: e.type, placeholder: e.placeholder, visible: e.offsetParent !== null}))",
        )
        for i in inputs:
            print(" ", i)

        # 找 tab 类元素：文本含 作品/书法/画谱/字形 的可点击元素
        print("\n=== 查找 tab 元素（含相关文本的可点击元素）===")
        tab_texts = page.eval_on_selector_all(
            "a, button, [role='tab'], div[onclick], span",
            """els => els.map(e => ({tag: e.tagName, text: (e.innerText||'').trim().substring(0,20), cls: e.className.substring(0,40)}))
               .filter(x => /作品|书法|画谱|字形|搜索|名画|绘画/.test(x.text))""",
        )
        for t in tab_texts[:30]:
            print(" ", t)

        # 尝试点击「作品」相关 tab
        print("\n=== 尝试点击作品搜索 tab ===")
        clicked = False
        for keyword in ["作品搜索", "作品", "书法", "名画", "绘画搜索"]:
            try:
                loc = page.get_by_text(keyword, exact=False).first
                if loc.count() > 0:
                    print(f"  找到「{keyword}」并点击")
                    loc.click(timeout=5000)
                    page.wait_for_timeout(1500)
                    clicked = True
                    break
            except Exception as e:
                print(f"  点击「{keyword}」失败: {e}")

        # 再次检查 input 可见性
        print("\n=== 点击后 input 可见性 ===")
        inputs2 = page.eval_on_selector_all(
            "input",
            "els => els.map((e,i) => ({i, type: e.type, placeholder: e.placeholder, visible: e.offsetParent !== null}))",
        )
        for i in inputs2:
            print(" ", i)

        # 找可见的、placeholder 含"作品"的搜索框并输入
        print("\n=== 输入「兰亭序」===")
        work_search = None
        for e in page.query_selector_all("input"):
            try:
                ph = e.get_attribute("placeholder") or ""
                if ("作品" in ph or "作者" in ph) and e.is_visible():
                    work_search = e
                    print(f"  找到作品搜索框: placeholder={ph}")
                    break
            except Exception:
                pass

        if work_search:
            work_search.click()
            page.wait_for_timeout(500)
            work_search.fill("兰亭序")
            page.wait_for_timeout(1000)
            page.keyboard.press("Enter")
            page.wait_for_timeout(9000)
        else:
            print("  未找到可见的作品搜索框，尝试对所有 input fill")
            for e in page.query_selector_all("input[type=text]"):
                try:
                    ph = e.get_attribute("placeholder") or ""
                    if "作品" in ph or "作者" in ph:
                        e.evaluate("el => el.style.display='block'")
                        e.fill("兰亭序")
                        page.keyboard.press("Enter")
                        page.wait_for_timeout(8000)
                        break
                except Exception:
                    pass

        print(f"\n=== 当前 URL: {page.url} ===")

        # 打印搜索相关 API
        print(f"\n=== 搜索 API 响应（共 {len(api_responses)} 条）===")
        for i, r in enumerate(api_responses):
            print(f"\n--- [{i}] {r['status']} {r['url']}")
            print(r["body"][:2500])

        page.screenshot(path="/tmp/ltfc_recon3.png", full_page=False)
        print("\n截图: /tmp/ltfc_recon3.png")
        browser.close()


if __name__ == "__main__":
    main()
