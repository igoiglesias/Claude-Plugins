---
description: "Browser automation skill: open pages, take screenshots, inspect HTML/DOM, check console & network errors, run Lighthouse audits, execute JavaScript, check accessibility, interact with elements"
---

# Browser DevTools Skill

You have access to a browser automation MCP server with the following tools. Use them whenever the user asks about opening pages, screenshots, HTML inspection, console errors, network issues, performance audits, accessibility checks, or any browser-related task.

## Workflow

Always follow this pattern:
1. **Open** → `browser_open(url)` first
2. **Inspect** → Use tools to gather information
3. **Close** → `browser_close()` when done to free resources

## Tool Reference

### Lifecycle
- `browser_open(url, headless=True, width=1920, height=1080, device="", wait_seconds=2)` — Open page. Devices: iphone_se, iphone_12, iphone_14, iphone_15_pro, pixel_7, galaxy_s23, ipad, ipad_pro
- `browser_close()` — Always call when done

### Capture
- `take_screenshot(output_path="", full_page=True, selector="")` — PNG screenshot
- `take_pdf(output_path="page.pdf")` — Save page as PDF (headless only)
- `get_page_html(selector="", outer=True)` — Get HTML source

### Inspect
- `get_page_info()` — Title, meta, headings, resource counts, performance timing
- `find_elements(selector, limit=25, attributes="text,href,src,class,id,alt,title,type,value,name")` — Query DOM
- `get_computed_styles(selector, properties="color,background-color,font-size,...")` — CSS computed values
- `get_console_logs(level="all", clear=False)` — Console output. Levels: all, error, severe, warning, info, debug
- `get_network_logs(filter_type="all", status_code=0, clear=False)` — Network. Filters: all, errors, failed, requests, responses

### Audit
- `run_lighthouse(url="", categories="performance,accessibility,best-practices,seo", device="mobile", output_path="")` — Lighthouse (needs npm lighthouse)
- `check_accessibility(url="")` — Quick a11y check (JS-based, no extra deps)

### Interact
- `click_element(selector, wait_seconds=1)` — Click element
- `fill_input(selector, value, clear_first=True, press_enter=False)` — Type in input
- `select_option(selector, value="", text="", index=-1)` — Select dropdown option
- `navigate(action="back|forward|refresh")` — Navigation
- `scroll_page(direction="down|up|top|bottom", pixels=600)` — Scroll
- `wait_for_element(selector, timeout=10, condition="visible|clickable|present|gone")` — Wait for DOM

### Other
- `run_javascript(code)` — Execute arbitrary JS. Use `return` for values.
- `manage_cookies(action="list|get|add|delete|clear", name="", value="", domain="")` — Cookies

## Tips

- For debugging, check `get_console_logs(level="error")` + `get_network_logs(filter_type="errors")` first
- Use `get_page_info()` for a quick overview before detailed inspection
- Save screenshots with `output_path` when the user needs files
- For responsive testing, use `device` parameter in `browser_open`
- `run_javascript` can do anything the DevTools console can do
- `take_pdf` only works in headless mode
