"""
Browser DevTools MCP Server for Claude Code Plugin
====================================================
External deps: selenium, mcp (FastMCP)
Everything else: Python stdlib (json, base64, os, subprocess, tempfile, time, logging, typing, pathlib, hashlib)
"""

import base64
import hashlib
import json
import logging
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from mcp.server.fastmcp import FastMCP

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
)

# ---------------------------------------------------------------------------
# Logging (stderr only — stdout reserved for MCP stdio transport)
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [browser-devtools] %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "Browser DevTools",
    description=(
        "Browser automation toolkit: open pages, screenshots, HTML extraction, "
        "console & network logs, Lighthouse audits, JS execution, accessibility "
        "checks, DOM inspection, element interaction, and more."
    ),
)

# ---------------------------------------------------------------------------
# Browser state (singleton per server process)
# ---------------------------------------------------------------------------
_driver: Optional[webdriver.Chrome] = None
_console_logs: list = []
_network_logs: list = []

# -- Mobile device presets (stdlib dict, no external dep) -------------------
_DEVICES = {
    "iphone_se": {"w": 375, "h": 667, "dpr": 2.0, "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"},
    "iphone_12": {"w": 390, "h": 844, "dpr": 3.0, "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"},
    "iphone_14": {"w": 393, "h": 852, "dpr": 3.0, "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"},
    "iphone_15_pro": {"w": 393, "h": 852, "dpr": 3.0, "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"},
    "pixel_7": {"w": 412, "h": 915, "dpr": 2.625, "ua": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"},
    "galaxy_s23": {"w": 360, "h": 780, "dpr": 3.0, "ua": "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"},
    "ipad": {"w": 810, "h": 1080, "dpr": 2.0, "ua": "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/604.1"},
    "ipad_pro": {"w": 1024, "h": 1366, "dpr": 2.0, "ua": "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/604.1"},
}


def _ok(**kw) -> str:
    return json.dumps({"status": "ok", **kw}, ensure_ascii=False)


def _err(msg: str) -> str:
    return json.dumps({"status": "error", "message": msg}, ensure_ascii=False)


def _need_browser() -> Optional[str]:
    if _driver is None:
        return _err("No browser session. Call browser_open first.")
    return None


# ---------------------------------------------------------------------------
# Browser lifecycle helpers
# ---------------------------------------------------------------------------
def _build_opts(headless: bool, width: int, height: int, device: Optional[str]) -> Options:
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-popup-blocking")
    opts.add_argument("--disable-infobars")
    opts.add_argument("--disable-notifications")
    opts.add_argument(f"--window-size={width},{height}")

    # Performance & network logging via Chrome DevTools Protocol
    opts.set_capability("goog:loggingPrefs", {"browser": "ALL", "performance": "ALL"})

    # Mobile emulation
    if device:
        key = device.lower().replace(" ", "_").replace("-", "_")
        d = _DEVICES.get(key)
        if d:
            opts.add_experimental_option("mobileEmulation", {
                "deviceMetrics": {"width": d["w"], "height": d["h"], "pixelRatio": d["dpr"]},
                "userAgent": d["ua"],
            })
    return opts


def _ensure_driver(headless=True, width=1920, height=1080, device=None) -> webdriver.Chrome:
    global _driver
    if _driver:
        try:
            _ = _driver.title
            return _driver
        except Exception:
            _driver = None

    opts = _build_opts(headless, width, height, device)
    _driver = webdriver.Chrome(options=opts)
    _driver.set_page_load_timeout(30)
    _driver.implicitly_wait(5)
    log.info("Chrome started (headless=%s, %dx%d, device=%s)", headless, width, height, device)
    return _driver


def _quit():
    global _driver, _console_logs, _network_logs
    if _driver:
        try:
            _driver.quit()
        except Exception:
            pass
        _driver = None
    _console_logs.clear()
    _network_logs.clear()


def _harvest_logs():
    """Collect console + network logs from Chrome DevTools Protocol."""
    global _console_logs, _network_logs
    if not _driver:
        return

    # Console logs
    try:
        for e in _driver.get_log("browser"):
            _console_logs.append({
                "level": e.get("level", ""),
                "message": e.get("message", ""),
                "timestamp": e.get("timestamp", 0),
                "source": e.get("source", ""),
            })
    except Exception:
        pass

    # Network logs from performance entries
    try:
        for e in _driver.get_log("performance"):
            try:
                msg = json.loads(e["message"])["message"]
                method = msg.get("method", "")
                if not method.startswith("Network."):
                    continue
                params = msg.get("params", {})
                entry = {"method": method, "ts": e.get("timestamp", 0)}

                if method == "Network.responseReceived":
                    r = params.get("response", {})
                    entry.update(url=r.get("url", ""), status=r.get("status", 0),
                                 mimeType=r.get("mimeType", ""), protocol=r.get("protocol", ""))
                elif method == "Network.requestWillBeSent":
                    r = params.get("request", {})
                    entry.update(url=r.get("url", ""), httpMethod=r.get("method", ""))
                elif method == "Network.loadingFailed":
                    entry.update(errorText=params.get("errorText", ""),
                                 type=params.get("type", ""),
                                 blocked=params.get("blockedReason", ""))
                else:
                    continue
                _network_logs.append(entry)
            except (json.JSONDecodeError, KeyError):
                pass
    except Exception:
        pass


# =========================================================================
# TOOLS — Browser Lifecycle
# =========================================================================

@mcp.tool()
def browser_open(
    url: str,
    headless: bool = True,
    width: int = 1920,
    height: int = 1080,
    device: str = "",
    wait_seconds: float = 2.0,
) -> str:
    """
    Open a URL in Chrome. Creates a new browser session or reuses the existing one.

    Args:
        url: Full URL to navigate to (e.g. https://example.com or http://localhost:3000)
        headless: Run without visible window (default True). Set False to see the browser.
        width: Viewport width in pixels (ignored when device is set)
        height: Viewport height in pixels (ignored when device is set)
        device: Mobile emulation preset: iphone_se, iphone_12, iphone_14, iphone_15_pro, pixel_7, galaxy_s23, ipad, ipad_pro
        wait_seconds: Seconds to wait after load for JS/SPA rendering (default 2)
    """
    try:
        drv = _ensure_driver(headless, width, height, device or None)
        drv.get(url)
        time.sleep(wait_seconds)
        _harvest_logs()
        return _ok(url=drv.current_url, title=drv.title)
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def browser_close() -> str:
    """Close the browser session and free all resources. Always call when done."""
    _quit()
    return _ok(message="Browser closed.")


# =========================================================================
# TOOLS — Screenshots
# =========================================================================

@mcp.tool()
def take_screenshot(
    output_path: str = "",
    full_page: bool = True,
    selector: str = "",
) -> str:
    """
    Capture a screenshot of the current page or a specific element.

    Args:
        output_path: Where to save the PNG file. If empty, returns base64 data.
        full_page: Capture the full scrollable page (default True)
        selector: CSS selector to capture only a specific element (e.g. '.hero', '#main')
    """
    if e := _need_browser():
        return e
    try:
        _harvest_logs()
        if selector:
            el = _driver.find_element(By.CSS_SELECTOR, selector)
            png = el.screenshot_as_png
        elif full_page:
            th = _driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
            tw = _driver.execute_script("return Math.max(document.body.scrollWidth, document.documentElement.scrollWidth)")
            orig = _driver.get_window_size()
            _driver.set_window_size(max(tw, 1920), th)
            time.sleep(0.5)
            png = _driver.get_screenshot_as_png()
            _driver.set_window_size(orig["width"], orig["height"])
        else:
            png = _driver.get_screenshot_as_png()

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(output_path).write_bytes(png)
            return _ok(path=str(Path(output_path).resolve()), size_bytes=len(png))

        b64 = base64.b64encode(png).decode()
        return _ok(base64_png=b64[:100] + f"...(total {len(b64)} chars)", size_bytes=len(png))
    except Exception as e:
        return _err(str(e))


# =========================================================================
# TOOLS — HTML & DOM
# =========================================================================

@mcp.tool()
def get_page_html(selector: str = "", outer: bool = True) -> str:
    """
    Get the HTML source of the page or a specific element.

    Args:
        selector: CSS selector (empty = entire page source)
        outer: True for outerHTML, False for innerHTML
    """
    if e := _need_browser():
        return e
    try:
        _harvest_logs()
        if selector:
            el = _driver.find_element(By.CSS_SELECTOR, selector)
            html = el.get_attribute("outerHTML" if outer else "innerHTML")
        else:
            html = _driver.page_source
        return _ok(html=html, length=len(html), url=_driver.current_url)
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def find_elements(
    selector: str,
    limit: int = 25,
    attributes: str = "text,href,src,class,id,alt,title,type,value,name",
) -> str:
    """
    Find all elements matching a CSS selector and extract their attributes.

    Args:
        selector: CSS selector (e.g. 'a', 'img', '.card', 'h1,h2,h3', 'input[type=email]')
        limit: Max elements to return (default 25)
        attributes: Comma-separated attributes to extract
    """
    if e := _need_browser():
        return e
    try:
        els = _driver.find_elements(By.CSS_SELECTOR, selector)
        attrs = [a.strip() for a in attributes.split(",")]
        results = []
        for el in els[:limit]:
            info = {"tag": el.tag_name}
            for a in attrs:
                v = el.text.strip() if a == "text" else el.get_attribute(a)
                if v:
                    info[a] = v[:500]
            info["visible"] = el.is_displayed()
            results.append(info)
        return _ok(selector=selector, total_found=len(els), returned=len(results), elements=results)
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def get_page_info() -> str:
    """
    Get comprehensive page metadata: title, URL, meta tags, heading structure,
    resource counts, viewport size, performance timing, cookie count, etc.
    """
    if e := _need_browser():
        return e
    try:
        _harvest_logs()
        info = _driver.execute_script("""
            const meta = {};
            document.querySelectorAll('meta').forEach(m => {
                const n = m.getAttribute('name') || m.getAttribute('property') || '';
                const c = m.getAttribute('content') || '';
                if (n && c) meta[n] = c.substring(0, 300);
            });
            const headings = {};
            ['h1','h2','h3','h4','h5','h6'].forEach(t => {
                const els = document.querySelectorAll(t);
                if (els.length) headings[t] = Array.from(els).slice(0,10).map(e => e.textContent.trim().substring(0,120));
            });
            const perf = performance.getEntriesByType('navigation')[0] || {};
            return {
                title: document.title,
                url: location.href,
                charset: document.characterSet,
                lang: document.documentElement.lang || '',
                meta: meta,
                headings: headings,
                counts: {
                    links: document.querySelectorAll('a[href]').length,
                    images: document.querySelectorAll('img').length,
                    scripts: document.querySelectorAll('script').length,
                    stylesheets: document.querySelectorAll('link[rel=stylesheet]').length,
                    forms: document.querySelectorAll('form').length,
                    inputs: document.querySelectorAll('input,select,textarea').length,
                    iframes: document.querySelectorAll('iframe').length,
                    buttons: document.querySelectorAll('button,[role=button]').length,
                    videos: document.querySelectorAll('video').length,
                },
                viewport: {
                    width: innerWidth, height: innerHeight,
                    scrollWidth: document.documentElement.scrollWidth,
                    scrollHeight: document.documentElement.scrollHeight,
                },
                timing: {
                    domContentLoaded: Math.round(perf.domContentLoadedEventEnd || 0),
                    loadComplete: Math.round(perf.loadEventEnd || 0),
                    domInteractive: Math.round(perf.domInteractive || 0),
                    ttfb: Math.round(perf.responseStart || 0),
                    transferSize: perf.transferSize || 0,
                },
                cookies: document.cookie.split(';').filter(c => c.trim()).length,
            };
        """)
        errs = sum(1 for l in _console_logs if l["level"] in ("SEVERE", "ERROR"))
        net_fails = sum(1 for l in _network_logs if l.get("method") == "Network.loadingFailed")
        return _ok(**info, console_errors=errs, network_failures=net_fails)
    except Exception as e:
        return _err(str(e))


# =========================================================================
# TOOLS — Console & Network Monitoring
# =========================================================================

@mcp.tool()
def get_console_logs(level: str = "all", clear: bool = False) -> str:
    """
    Get browser console logs (errors, warnings, info, debug).

    Args:
        level: Filter: all, error, severe, warning, info, debug
        clear: Clear the log buffer after retrieval
    """
    if e := _need_browser():
        return e
    _harvest_logs()
    if level == "all":
        filtered = _console_logs
    else:
        lu = level.upper()
        filtered = [l for l in _console_logs if l["level"].upper() == lu]
    result = _ok(total=len(_console_logs), filtered=len(filtered), level_filter=level, logs=filtered[-200:])
    if clear:
        _console_logs.clear()
    return result


@mcp.tool()
def get_network_logs(filter_type: str = "all", status_code: int = 0, clear: bool = False) -> str:
    """
    Get network request/response logs.

    Args:
        filter_type: all, errors (4xx/5xx), failed, requests, responses
        status_code: Filter by specific HTTP status code (0 = no filter)
        clear: Clear the network log buffer after retrieval
    """
    if e := _need_browser():
        return e
    _harvest_logs()
    filtered = _network_logs
    if filter_type == "errors":
        filtered = [l for l in filtered if l.get("status", 0) >= 400]
    elif filter_type == "failed":
        filtered = [l for l in filtered if l.get("method") == "Network.loadingFailed"]
    elif filter_type == "requests":
        filtered = [l for l in filtered if l.get("method") == "Network.requestWillBeSent"]
    elif filter_type == "responses":
        filtered = [l for l in filtered if l.get("method") == "Network.responseReceived"]
    if status_code > 0:
        filtered = [l for l in filtered if l.get("status") == status_code]
    result = _ok(total=len(_network_logs), filtered=len(filtered), filter=filter_type, logs=filtered[-300:])
    if clear:
        _network_logs.clear()
    return result


# =========================================================================
# TOOLS — JavaScript Execution
# =========================================================================

@mcp.tool()
def run_javascript(code: str) -> str:
    """
    Execute JavaScript in the page context and return the result.

    Args:
        code: JS code. Use 'return ...' to get a value back.
              Examples:
                "return document.title"
                "return document.querySelectorAll('a').length"
                "return JSON.stringify(performance.timing)"
                "document.querySelector('.btn').click()"
    """
    if e := _need_browser():
        return e
    try:
        result = _driver.execute_script(code)
        if result is None:
            serialized = None
        elif isinstance(result, (str, int, float, bool)):
            serialized = result
        elif isinstance(result, list):
            serialized = [str(x)[:500] for x in result[:100]]
        elif isinstance(result, dict):
            serialized = {str(k): str(v)[:500] for k, v in list(result.items())[:50]}
        else:
            serialized = str(result)[:2000]
        return _ok(result=serialized)
    except Exception as e:
        return _err(str(e))


# =========================================================================
# TOOLS — Lighthouse Audit
# =========================================================================

@mcp.tool()
def run_lighthouse(
    url: str = "",
    categories: str = "performance,accessibility,best-practices,seo",
    device: str = "mobile",
    output_path: str = "",
) -> str:
    """
    Run a Google Lighthouse audit. Requires Node.js + lighthouse CLI (npm i -g lighthouse).

    Args:
        url: URL to audit (empty = current browser URL)
        categories: Comma-separated: performance, accessibility, best-practices, seo
        device: 'mobile' or 'desktop'
        output_path: Save full HTML report to this path (optional)
    """
    target = url or (_driver.current_url if _driver else "")
    if not target:
        return _err("No URL provided and no browser session open.")

    # Check lighthouse availability
    try:
        subprocess.run(["lighthouse", "--version"], capture_output=True, timeout=10)
    except FileNotFoundError:
        return _err("Lighthouse CLI not found. Install: npm install -g lighthouse")

    try:
        with tempfile.TemporaryDirectory() as tmp:
            base = os.path.join(tmp, "report")
            cmd = [
                "lighthouse", target,
                f"--only-categories={categories}",
                f"--form-factor={device}",
                "--output=json,html",
                f"--output-path={base}",
                "--chrome-flags=--headless=new --no-sandbox --disable-dev-shm-usage --disable-gpu",
                "--quiet",
            ]
            if device == "desktop":
                cmd.append("--preset=desktop")

            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if proc.returncode != 0:
                return _err(f"Lighthouse failed: {proc.stderr[:500]}")

            with open(base + ".report.json", "r") as f:
                report = json.load(f)

            scores = {}
            for k, v in report.get("categories", {}).items():
                scores[k] = {"score": round((v.get("score") or 0) * 100), "title": v.get("title", k)}

            metrics = {}
            for key in ["first-contentful-paint", "largest-contentful-paint", "total-blocking-time",
                        "cumulative-layout-shift", "speed-index", "interactive"]:
                a = report.get("audits", {}).get(key)
                if a:
                    metrics[key] = {"value": a.get("displayValue", ""), "score": round((a.get("score") or 0) * 100)}

            if output_path:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                html_file = base + ".report.html"
                if os.path.exists(html_file):
                    Path(output_path).write_text(Path(html_file).read_text())

            result = _ok(url=target, device=device, scores=scores, metrics=metrics)
            if output_path:
                result_dict = json.loads(result)
                result_dict["report_path"] = str(Path(output_path).resolve())
                return json.dumps(result_dict, ensure_ascii=False)
            return result
    except subprocess.TimeoutExpired:
        return _err("Lighthouse timed out after 120 seconds.")
    except Exception as e:
        return _err(str(e))


# =========================================================================
# TOOLS — Accessibility Check (pure JS, no external dep)
# =========================================================================

@mcp.tool()
def check_accessibility(url: str = "") -> str:
    """
    Quick accessibility audit using JavaScript: missing alt text, empty links,
    missing form labels, heading hierarchy, lang attribute, ARIA issues, contrast hints.

    Args:
        url: Navigate to this URL first (optional — uses current page if empty)
    """
    if e := _need_browser():
        return e
    try:
        if url:
            _driver.get(url)
            time.sleep(2)

        issues = _driver.execute_script("""
            const issues = [];
            // Missing alt text
            document.querySelectorAll('img').forEach(img => {
                if (img.getAttribute('alt') === null) {
                    issues.push({type:'missing-alt', severity:'error', el:img.outerHTML.substring(0,150), msg:'Image missing alt attribute'});
                } else if (img.alt.trim() === '' && !img.getAttribute('role')) {
                    issues.push({type:'empty-alt', severity:'warning', el:img.outerHTML.substring(0,150), msg:'Image has empty alt (OK only if decorative)'});
                }
            });
            // Empty links
            document.querySelectorAll('a').forEach(a => {
                if (!a.textContent.trim() && !a.getAttribute('aria-label') && !a.querySelector('img[alt]')) {
                    issues.push({type:'empty-link', severity:'error', el:a.outerHTML.substring(0,150), msg:'Link has no accessible text'});
                }
            });
            // Form inputs without labels
            document.querySelectorAll('input,select,textarea').forEach(inp => {
                if (['hidden','submit','button','reset','image'].includes(inp.type)) return;
                const id = inp.id;
                if (!id || !document.querySelector('label[for=\"'+id+'\"]')) {
                    if (!inp.getAttribute('aria-label') && !inp.getAttribute('aria-labelledby') && !inp.getAttribute('placeholder')) {
                        issues.push({type:'missing-label', severity:'error', el:inp.outerHTML.substring(0,150), msg:'Input missing label/aria-label'});
                    }
                }
            });
            // Heading hierarchy
            let prev = 0;
            document.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(h => {
                const lvl = parseInt(h.tagName[1]);
                if (prev > 0 && lvl - prev > 1) {
                    issues.push({type:'heading-skip', severity:'warning', el:`<${h.tagName.toLowerCase()}>${h.textContent.trim().substring(0,80)}`, msg:`Heading skipped: h${prev} → h${lvl}`});
                }
                prev = lvl;
            });
            // Multiple h1
            const h1s = document.querySelectorAll('h1');
            if (h1s.length > 1) issues.push({type:'multiple-h1', severity:'warning', el:'', msg:`Found ${h1s.length} h1 elements (should be 1)`});
            if (h1s.length === 0) issues.push({type:'no-h1', severity:'warning', el:'', msg:'No h1 element found'});
            // Missing lang
            if (!document.documentElement.lang) issues.push({type:'missing-lang', severity:'error', el:'<html>', msg:'Missing lang attribute'});
            // Missing title
            if (!document.title.trim()) issues.push({type:'missing-title', severity:'error', el:'<title>', msg:'Page has no title'});
            // Buttons without accessible name
            document.querySelectorAll('button,[role=button]').forEach(btn => {
                if (!btn.textContent.trim() && !btn.getAttribute('aria-label') && !btn.getAttribute('title')) {
                    issues.push({type:'empty-button', severity:'error', el:btn.outerHTML.substring(0,150), msg:'Button has no accessible name'});
                }
            });
            // Tabindex > 0 (anti-pattern)
            document.querySelectorAll('[tabindex]').forEach(el => {
                const ti = parseInt(el.getAttribute('tabindex'));
                if (ti > 0) issues.push({type:'positive-tabindex', severity:'warning', el:el.outerHTML.substring(0,150), msg:`tabindex=${ti} disrupts natural tab order`});
            });
            return issues;
        """)

        errors = sum(1 for i in issues if i["severity"] == "error")
        warnings = sum(1 for i in issues if i["severity"] == "warning")
        return _ok(url=_driver.current_url, total_issues=len(issues), errors=errors, warnings=warnings, issues=issues[:60])
    except Exception as e:
        return _err(str(e))


# =========================================================================
# TOOLS — Interaction
# =========================================================================

@mcp.tool()
def click_element(selector: str, wait_seconds: float = 1.0) -> str:
    """
    Click an element on the page.

    Args:
        selector: CSS selector of the element to click
        wait_seconds: Seconds to wait after clicking for page changes
    """
    if e := _need_browser():
        return e
    try:
        el = WebDriverWait(_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        el.click()
        time.sleep(wait_seconds)
        _harvest_logs()
        return _ok(clicked=selector, url=_driver.current_url)
    except TimeoutException:
        return _err(f"Element not clickable within 10s: {selector}")
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def fill_input(selector: str, value: str, clear_first: bool = True, press_enter: bool = False) -> str:
    """
    Type text into a form field.

    Args:
        selector: CSS selector of the input/textarea
        value: Text to type
        clear_first: Clear existing content first (default True)
        press_enter: Press Enter after typing (default False)
    """
    if e := _need_browser():
        return e
    try:
        el = WebDriverWait(_driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        if clear_first:
            el.clear()
        el.send_keys(value)
        if press_enter:
            el.send_keys(Keys.RETURN)
            time.sleep(1)
        return _ok(selector=selector, typed=len(value))
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def select_option(selector: str, value: str = "", text: str = "", index: int = -1) -> str:
    """
    Select an option from a <select> dropdown.

    Args:
        selector: CSS selector of the <select> element
        value: Option value attribute to select
        text: Visible text of the option to select
        index: Index of the option (0-based). Use -1 to skip.
    """
    if e := _need_browser():
        return e
    try:
        from selenium.webdriver.support.ui import Select
        el = _driver.find_element(By.CSS_SELECTOR, selector)
        sel = Select(el)
        if value:
            sel.select_by_value(value)
        elif text:
            sel.select_by_visible_text(text)
        elif index >= 0:
            sel.select_by_index(index)
        return _ok(selector=selector, selected=sel.first_selected_option.text)
    except Exception as e:
        return _err(str(e))


# =========================================================================
# TOOLS — Navigation & Scroll
# =========================================================================

@mcp.tool()
def navigate(action: str = "back") -> str:
    """
    Browser navigation: back, forward, or refresh.

    Args:
        action: 'back', 'forward', or 'refresh'
    """
    if e := _need_browser():
        return e
    try:
        {"back": _driver.back, "forward": _driver.forward, "refresh": _driver.refresh}[action]()
        time.sleep(1)
        _harvest_logs()
        return _ok(action=action, url=_driver.current_url, title=_driver.title)
    except KeyError:
        return _err(f"Unknown action: {action}. Use back, forward, or refresh.")
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def scroll_page(direction: str = "down", pixels: int = 600) -> str:
    """
    Scroll the page.

    Args:
        direction: 'up', 'down', 'top', 'bottom'
        pixels: Pixels to scroll (for up/down)
    """
    if e := _need_browser():
        return e
    try:
        js = {
            "down": f"window.scrollBy(0,{pixels})",
            "up": f"window.scrollBy(0,-{pixels})",
            "top": "window.scrollTo(0,0)",
            "bottom": "window.scrollTo(0,document.body.scrollHeight)",
        }.get(direction)
        if not js:
            return _err("Direction must be up, down, top, or bottom.")
        _driver.execute_script(js)
        time.sleep(0.3)
        pos = _driver.execute_script("return window.pageYOffset")
        return _ok(direction=direction, scroll_y=pos)
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def wait_for_element(selector: str, timeout: int = 10, condition: str = "visible") -> str:
    """
    Wait for an element to meet a condition on the page.

    Args:
        selector: CSS selector
        timeout: Max seconds to wait
        condition: 'visible', 'clickable', 'present', or 'gone'
    """
    if e := _need_browser():
        return e
    try:
        w = WebDriverWait(_driver, timeout)
        conds = {
            "visible": EC.visibility_of_element_located,
            "clickable": EC.element_to_be_clickable,
            "present": EC.presence_of_element_located,
            "gone": EC.invisibility_of_element_located,
        }
        fn = conds.get(condition)
        if not fn:
            return _err(f"Unknown condition: {condition}")
        fn(w, (By.CSS_SELECTOR, selector)) if condition == "gone" else w.until(fn((By.CSS_SELECTOR, selector)))
        return _ok(selector=selector, condition=condition)
    except TimeoutException:
        return _ok(status="timeout", selector=selector, condition=condition, message=f"Timed out after {timeout}s")
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def manage_cookies(action: str = "list", name: str = "", value: str = "", domain: str = "") -> str:
    """
    Manage browser cookies.

    Args:
        action: 'list', 'get', 'add', 'delete', 'clear'
        name: Cookie name (for get/add/delete)
        value: Cookie value (for add)
        domain: Cookie domain (for add)
    """
    if e := _need_browser():
        return e
    try:
        if action == "list":
            return _ok(cookies=_driver.get_cookies())
        elif action == "get":
            c = _driver.get_cookie(name)
            return _ok(cookie=c) if c else _err(f"Cookie '{name}' not found")
        elif action == "add":
            cookie = {"name": name, "value": value}
            if domain:
                cookie["domain"] = domain
            _driver.add_cookie(cookie)
            return _ok(added=name)
        elif action == "delete":
            _driver.delete_cookie(name)
            return _ok(deleted=name)
        elif action == "clear":
            _driver.delete_all_cookies()
            return _ok(message="All cookies cleared")
        return _err(f"Unknown action: {action}")
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def take_pdf(output_path: str = "page.pdf") -> str:
    """
    Save the current page as a PDF (headless Chrome only).

    Args:
        output_path: Where to save the PDF file
    """
    if e := _need_browser():
        return e
    try:
        result = _driver.execute_cdp_cmd("Page.printToPDF", {
            "landscape": False,
            "printBackground": True,
            "preferCSSPageSize": True,
        })
        pdf_bytes = base64.b64decode(result["data"])
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(pdf_bytes)
        return _ok(path=str(Path(output_path).resolve()), size_bytes=len(pdf_bytes))
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def get_computed_styles(selector: str, properties: str = "color,background-color,font-size,font-family,margin,padding,display,position") -> str:
    """
    Get computed CSS styles of an element.

    Args:
        selector: CSS selector
        properties: Comma-separated CSS property names to inspect
    """
    if e := _need_browser():
        return e
    try:
        props = [p.strip() for p in properties.split(",")]
        styles = _driver.execute_script("""
            const el = document.querySelector(arguments[0]);
            if (!el) return null;
            const cs = getComputedStyle(el);
            const result = {};
            arguments[1].forEach(p => { result[p] = cs.getPropertyValue(p); });
            result._tag = el.tagName.toLowerCase();
            result._rect = el.getBoundingClientRect().toJSON();
            return result;
        """, selector, props)
        if styles is None:
            return _err(f"Element not found: {selector}")
        return _ok(selector=selector, styles=styles)
    except Exception as e:
        return _err(str(e))


# =========================================================================
# Entry point
# =========================================================================

if __name__ == "__main__":
    mcp.run(transport="stdio")
