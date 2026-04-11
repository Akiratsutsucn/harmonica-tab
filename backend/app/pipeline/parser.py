"""Jianpu page parser for 2qupu.com."""
import logging
import re

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

BASE_URL = "https://www.2qupu.com"


def parse_search_results(html: str) -> list[dict]:
    """Parse 2qupu.com search results page. Returns list of {title, url}."""
    soup = BeautifulSoup(html, "lxml")
    results = []
    for a in soup.find_all("a", href=re.compile(r"/kouqin/\d{8}/\d+\.html")):
        title = re.sub(r"<[^>]+>", "", a.decode_contents()).strip()
        href = a.get("href", "")
        if title and href:
            url = href if href.startswith("http") else BASE_URL + href
            results.append({"title": title, "url": url})
    return results


def parse_detail_page(html: str) -> dict:
    """Parse 2qupu.com detail page. Returns {title, artist, images}."""
    soup = BeautifulSoup(html, "lxml")

    title = ""
    artist = ""

    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)

    page_title = soup.find("title")
    if page_title:
        text = page_title.get_text()
        m = re.match(r"(.+?)口琴谱", text)
        if m:
            raw = m.group(1).strip()
            am = re.search(r"[（(](.+?)[）)]", raw)
            if am:
                artist = am.group(1).strip()
        if not title:
            title = text.replace("口琴谱", "").replace("-口琴曲谱-爱曲谱网", "").strip()

    images = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and "file.2qupu.com" in src and any(ext in src.lower() for ext in (".jpg", ".png", ".gif")):
            images.append(src)

    return {"title": title, "artist": artist, "images": images[:5]}
