---
name: audit
description: "Run a full audit on a URL: screenshot, console errors, network errors, accessibility, and Lighthouse scores"
---

Run a comprehensive browser audit on the provided URL. Follow these exact steps:

1. Open the URL with `browser_open`
2. Get page info with `get_page_info` — report title, meta, resource counts, timing
3. Check console logs with `get_console_logs(level="error")` — list all errors
4. Check network with `get_network_logs(filter_type="errors")` — list all 4xx/5xx responses
5. Check network failures with `get_network_logs(filter_type="failed")` — list failed requests
6. Run accessibility check with `check_accessibility` — list issues
7. Take a full-page screenshot with `take_screenshot(output_path="audit-screenshot.png")`
8. If Lighthouse is available, run `run_lighthouse` and report scores
9. Close with `browser_close`

Present results as a clear, organized report with sections for each check.
If no URL is provided by the user, ask for one.
