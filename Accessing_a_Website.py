#!/usr/bin/env python3
"""
open_aiche_annotated.py — Fully annotated version of a script that opens a web browser
and navigates to https://www.aiche.org (AIChE). It supports two modes:
  1) Standard library `webbrowser` (no extra installs).
  2) Selenium automation with optional headless mode and auto driver management.

Run examples:
  python open_aiche_annotated.py
  python open_aiche_annotated.py --selenium chrome
  python open_aiche_annotated.py --selenium edge
  python open_aiche_annotated.py --selenium firefox
  python open_aiche_annotated.py --selenium chrome --headless

Dependencies for Selenium mode:
  pip install selenium webdriver-manager

Notes:
- This file is intentionally verbose with comments, explaining each line and choice.
- The canonical AIChE domain is .org; .com typically redirects.
"""

# -------------------------
# Standard library imports
# -------------------------
import argparse          # Build a friendly command-line interface (CLI).
import sys               # For sys.stderr (error output) and sys.exit (exit codes).
import time              # For sleep() to keep a visible browser open briefly.
import webbrowser        # Lightweight way to open URLs in the user's default browser.

# ---------------------------------------------
# Configuration: keep key values in one place.
# ---------------------------------------------
URL = "https://www.aiche.org"  # Canonical AIChE domain; servers may redirect .com -> .org.

def open_with_webbrowser():
    """
    Use Python's standard library to open the default browser.
    This path requires no external dependencies and works on Windows/macOS/Linux.
    """
    # Provide feedback so the user knows what's happening.
    print(f"Opening {URL} in your default browser...")
    # webbrowser.open asks the OS to open the URL. new=2 tries for a new tab (if supported).
    ok = webbrowser.open(URL, new=2)  # 2 = new tab; falls back to a new window/platform default.

    # Some platforms/browsers may return False if they cannot be launched.
    if not ok:
        # Print to standard error stream so tools/CI can distinguish normal output from errors.
        print("Could not open the browser using the standard library.", file=sys.stderr)
        # Exit code 1 signals a general failure for this mode.
        sys.exit(1)

def open_with_selenium(browser: str, headless: bool):
    """
    Launch a real browser controlled by Selenium WebDriver. Supports Chrome, Edge, and Firefox.
    If headless=True, no visible window is shown (useful for automation/CI).

    We import Selenium and driver-managers inside the function so the module can still be used
    without Selenium installed (e.g., when using only the standard library mode).
    """
    try:
        # Core Selenium WebDriver APIs.
        from selenium import webdriver
        # Per-browser "Service" classes wire up the driver binary to Selenium.
        from selenium.webdriver.chrome.service import Service as ChromeService
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from selenium.webdriver.edge.service import Service as EdgeService
        # Locators and wait utilities for reliable page-load checks.
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        # Driver managers auto-download the correct driver for your installed browser.
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.firefox import GeckoDriverManager
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
    except Exception as e:
        # If these imports fail, tell the user how to install dependencies and exit with code 2.
        print("Selenium (and/or webdriver-manager) is not installed.",
              "Run: pip install selenium webdriver-manager",
              f"\nOriginal error: {e}", sep="\n", file=sys.stderr)
        sys.exit(2)

    # We'll assign the driver into this variable; initializing to None makes it visible in finally.
    driver = None
    try:
        # Normalize the browser name to simplify comparisons and accept CHROME/Chrome/chrome, etc.
        browser = browser.lower()

        # ----------------------
        # Google Chrome branch
        # ----------------------
        if browser == "chrome":
            options = webdriver.ChromeOptions()        # Container for Chrome-specific flags.
            if headless:
                # Chrome's modern headless mode with better parity to headed mode.
                options.add_argument("--headless=new")
            # Start maximized for friendlier screenshots/visibility (ignored in some headless envs).
            options.add_argument("--start-maximized")
            # ChromeDriverManager installs or locates a matching chromedriver binary automatically.
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )

        # ------------------
        # Microsoft Edge
        # ------------------
        elif browser == "edge":
            options = webdriver.EdgeOptions()          # Edge-specific flags.
            if headless:
                options.add_argument("--headless=new") # Edge shares Chromium headless semantics.
            options.add_argument("--start-maximized")
            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=options
            )

        # ----------------------
        # Mozilla Firefox branch
        # ----------------------
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()       # Firefox-specific flags.
            if headless:
                # Firefox uses "-headless" (single dash), different from Chromium.
                options.add_argument("-headless")
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
            # On some platforms, maximize after launch; in headless this can be a no-op/raise.
            try:
                driver.maximize_window()
            except Exception:
                pass  # It's okay if maximizing fails in virtual/headless environments.

        else:
            # Reject anything other than the allowed choices.
            print(f"Unknown browser '{browser}'. Use chrome, edge, or firefox.", file=sys.stderr)
            sys.exit(3)

        # Status print before navigation so users/logs show what's happening.
        print(f"Launching {browser} and navigating to {URL} ...")

        # Navigate to the target page. This returns once initial navigation completes;
        # it does not guarantee that all dynamic content finished loading.
        driver.get(URL)

        # --------------------
        # Basic "page is up" wait
        # --------------------
        # We wait until a <body> element exists. It's a generic, reliable signal that
        # the DOM was built. For more specific checks, wait on site-specific elements.
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except Exception:
            # If this times out, continue anyway—network blockers or cookie modals can interfere.
            pass

        # Quick sanity check: print the current page title to stdout.
        print("Page title:", driver.title)

        # ----------------
        # Optional proof
        # ----------------
        # Save a screenshot to confirm visually that we reached the site.
        screenshot_path = "aiche_home.png"
        try:
            driver.save_screenshot(screenshot_path)
            print(f"Saved screenshot to {screenshot_path}")
        except Exception:
            # Not all environments permit screenshots; it's non-fatal.
            pass

        # If the browser is visible (not headless), keep it open briefly so humans can see it
        # before the script ends (some automation wrappers would close immediately otherwise).
        if not headless:
            print("Leaving the browser open for 5 seconds...")
            time.sleep(5)

    finally:
        # Cleanup policy: in headless mode we always quit to avoid orphaned processes.
        # In visible mode, we intentionally DO NOT quit so the user can interact with the page.
        if headless and driver is not None:
            driver.quit()

def main():
    """
    Parse command-line flags and dispatch to either the standard-library or Selenium path.
    Using a `main()` function and the `if __name__ == "__main__"` guard makes the module
    safe to import without side effects.
    """
    # Create a parser with a helpful description shown in -h/--help.
    parser = argparse.ArgumentParser(description="Open a navigator and access aiche.com")

    # Optional flag to choose Selenium and select which browser to automate.
    # argparse enforces the allowed choices and shows them in the help text.
    parser.add_argument("--selenium", choices=["chrome", "edge", "firefox"],
                        help="Use Selenium to automate a specific browser")

    # Boolean flag; if present, it's True (default False). Only meaningful with --selenium.
    parser.add_argument("--headless", action="store_true",
                        help="Run the Selenium browser without a visible window")

    # Parse the flags from sys.argv.
    args = parser.parse_args()

    # If --selenium was provided, run the automated path; otherwise, use the simple webbrowser path.
    if args.selenium:
        open_with_selenium(args.selenium, args.headless)
    else:
        open_with_webbrowser()

# Entry-point guard: execute main() only when the file is run directly, not when imported.
if __name__ == "__main__":
    main()
