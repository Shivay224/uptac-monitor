def fetch():
    notices = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, timeout=60000)

        # wait full JS render
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(8000)

        # instead of table → grab visible cards/divs
        elements = page.locator(".card, .table tr, .container-fluid a")

        count = elements.count()

        seen = set()

        for i in range(count):
            el = elements.nth(i)
            text = el.inner_text().strip()

            if len(text) < 10:
                continue

            # try to find link
            link = URL
            try:
                href = el.get_attribute("href")
                if href:
                    link = href
            except:
                pass

            # dedup by text
            if text in seen:
                continue
            seen.add(text)

            notices.append({
                "title": text,
                "published": "",
                "link": link
            })

        browser.close()

    return notices
