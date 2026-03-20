---
name: debug
description: "Open a URL and diagnose console errors, network failures, and JS exceptions"
---

Debug a web page for errors. Steps:

1. Open the URL with `browser_open`
2. Wait a moment for dynamic content to load
3. Get `get_console_logs(level="error")` — show all console errors with full messages
4. Get `get_console_logs(level="warning")` — show warnings
5. Get `get_network_logs(filter_type="errors")` — show all HTTP 4xx/5xx responses with URLs
6. Get `get_network_logs(filter_type="failed")` — show completely failed requests (blocked, CORS, DNS, etc.)
7. Run `get_page_info()` to check for basic issues (missing title, meta, etc.)
8. Close with `browser_close`

For each error found, explain:
- What the error means
- Likely cause
- How to fix it

If no errors are found, confirm the page is clean and report the page load timing.
