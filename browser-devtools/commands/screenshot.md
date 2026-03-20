---
name: screenshot
description: "Take a screenshot of a URL (optionally: full page, mobile device, specific element)"
---

Take a screenshot of the URL provided by the user. Steps:

1. Open the URL with `browser_open`. If the user mentions a device (mobile, iPhone, iPad, Pixel, etc.), use the `device` parameter.
2. Take a screenshot with `take_screenshot(output_path="screenshot.png", full_page=True)`. If the user asked for a specific element, use the `selector` parameter.
3. Close with `browser_close`

If the user wants multiple device screenshots, repeat with different devices (e.g., iphone_14, ipad, desktop at 1920x1080).
