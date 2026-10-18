"""
Playwright screenshot and video capture script for Blast Radius Brain.
Captures screenshots 01 to 07 at 1920x1080 and records video in capture/video_raw/.
"""

import os
import sys
import time
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "capture", "screenshots")
VIDEO_RAW_DIR = os.path.join(BASE_DIR, "capture", "video_raw")

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(VIDEO_RAW_DIR, exist_ok=True)


def capture_all():
    with sync_playwright() as p:
        print("Launching Chromium (1920x1080)...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=VIDEO_RAW_DIR,
            record_video_size={"width": 1920, "height": 1080},
        )
        page = context.new_page()

        # ---------------------------------------------------------
        # 1. 01_home.png
        # ---------------------------------------------------------
        print("1/7: Capturing 01_home.png...")
        page.goto("http://localhost:8501", wait_until="networkidle")
        page.wait_for_selector("text=Blast Radius Brain", timeout=20000)
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "01_home.png"), full_page=True)
        print(" -> Saved 01_home.png")

        # ---------------------------------------------------------
        # 2. 02_blast_radius.png
        # ---------------------------------------------------------
        print("2/7: Capturing 02_blast_radius.png...")
        btn_blast = page.locator("button:has-text('What breaks if ledger-service goes down?')")
        if btn_blast.count() > 0:
            btn_blast.first.click()
        else:
            input_box = page.locator("input[type='text']").first
            input_box.fill("What breaks if ledger-service goes down?")
            input_box.press("Enter")
            page.locator("button:has-text('Execute Graph Query')").first.click()

        page.wait_for_selector("text=Graph Traversal Answer", timeout=15000)
        page.wait_for_selector("text=checkout-ui", timeout=10000)
        page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "02_blast_radius.png"), full_page=True)
        print(" -> Saved 02_blast_radius.png")

        # ---------------------------------------------------------
        # 3. 03_expert_finder.png
        # ---------------------------------------------------------
        print("3/7: Capturing 03_expert_finder.png...")
        btn_expert = page.locator("button:has-text('Who knows ledger-service best?')")
        if btn_expert.count() > 0:
            btn_expert.first.click()
        else:
            input_box = page.locator("input[type='text']").first
            input_box.fill("Who knows ledger-service best?")
            input_box.press("Enter")
            page.locator("button:has-text('Execute Graph Query')").first.click()

        page.wait_for_selector("text=Maya Chen", timeout=15000)
        page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "03_expert_finder.png"), full_page=True)
        print(" -> Saved 03_expert_finder.png")

        # ---------------------------------------------------------
        # 4. 04_decision.png
        # ---------------------------------------------------------
        print("4/7: Capturing 04_decision.png...")
        btn_dec = page.locator("button:has-text('Who decided to pause Helios?')")
        if btn_dec.count() > 0:
            btn_dec.first.click()
        else:
            input_box = page.locator("input[type='text']").first
            input_box.fill("Who decided to pause Helios?")
            input_box.press("Enter")
            page.locator("button:has-text('Execute Graph Query')").first.click()

        page.wait_for_selector("text=Nora Haddad", timeout=15000)
        page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "04_decision.png"), full_page=True)
        print(" -> Saved 04_decision.png")

        # ---------------------------------------------------------
        # 5. 05_honest_unknown.png
        # ---------------------------------------------------------
        print("5/7: Capturing 05_honest_unknown.png...")
        page.goto("http://localhost:8501", wait_until="networkidle")
        page.wait_for_selector("text=Blast Radius Brain", timeout=15000)
        page.wait_for_timeout(1000)

        input_box = page.locator("input[type='text']").first
        input_box.fill("Who owns Project Phoenix?")
        input_box.press("Enter")
        submit_btn = page.locator("button:has-text('Execute Graph Query')").first
        if submit_btn.count() > 0:
            submit_btn.click()

        page.wait_for_selector("text=I could not classify your query", timeout=15000)
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "05_honest_unknown.png"), full_page=True)
        print(" -> Saved 05_honest_unknown.png")

        # ---------------------------------------------------------
        # 6. 06_graph_browser.png & 7. 07_graph_ledger_highlight.png
        # ---------------------------------------------------------
        print("6/7 & 7/7: Connecting to FalkorDB Browser at http://localhost:3000...")
        try:
            page.goto("http://localhost:3000", wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(1500)

            # Log in if needed
            login_btn = page.locator("button:has-text('Log in')")
            if login_btn.count() > 0:
                login_btn.first.click()
                page.wait_for_timeout(2500)

            # Dismiss tutorial overlay if present
            page.evaluate("""() => {
                document.querySelectorAll('[data-tutorial-overlay], [data-testid="tutorialSpotlight"]').forEach(e => e.remove());
                const btns = Array.from(document.querySelectorAll('button'));
                const skip = btns.find(b => b.innerText.toLowerCase().includes('skip'));
                if (skip) skip.click();
            }""")
            page.wait_for_timeout(1000)

            # Select Graph: company
            select_graph = page.locator("text=Select Graph")
            if select_graph.count() > 0:
                select_graph.first.click(force=True)
                page.wait_for_timeout(1000)
                company_opt = page.locator("text=company")
                if company_opt.count() > 0:
                    company_opt.first.click(force=True)
                    page.wait_for_timeout(2000)

            # Dismiss any remaining overlays
            page.evaluate("""() => {
                document.querySelectorAll('[data-tutorial-overlay], [data-testid="tutorialSpotlight"]').forEach(e => e.remove());
            }""")

            # Query 1: All nodes for 06_graph_browser.png
            query_box = page.locator("textarea, .monaco-editor, input[type='text']").first
            if query_box.count() > 0:
                query_box.click(force=True)
                page.keyboard.press("Control+A")
                page.keyboard.type("MATCH (n) RETURN n LIMIT 35")
                run_btn = page.locator("button:has-text('RUN'), button:has-text('Run')").first
                if run_btn.count() > 0:
                    run_btn.click(force=True)
                else:
                    page.keyboard.press("Enter")
                page.wait_for_timeout(4000)

            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "06_graph_browser.png"), full_page=True)
            print(" -> Saved 06_graph_browser.png")

            # Query 2: Highlight blast radius subgraph for 07_graph_ledger_highlight.png
            if query_box.count() > 0:
                query_box.click(force=True)
                page.keyboard.press("Control+A")
                page.keyboard.type("MATCH path = (s:System {name: 'ledger-service'})<-[:DEPENDS_ON*1..5]-(downstream:System) RETURN path")
                run_btn = page.locator("button:has-text('RUN'), button:has-text('Run')").first
                if run_btn.count() > 0:
                    run_btn.click(force=True)
                else:
                    page.keyboard.press("Enter")
                page.wait_for_timeout(4000)

            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "07_graph_ledger_highlight.png"), full_page=True)
            print(" -> Saved 07_graph_ledger_highlight.png")

        except Exception as e:
            print(f"Notice during FalkorDB browser interaction: {e}")
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "06_graph_browser.png"), full_page=True)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "07_graph_ledger_highlight.png"), full_page=True)

        context.close()
        browser.close()
        print("All screenshots captured and Playwright raw video flushed!")


if __name__ == "__main__":
    capture_all()
