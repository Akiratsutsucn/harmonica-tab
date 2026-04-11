"""Jianpu page parser for jianpu.cn."""
import logging
import re

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def parse_search_results(html: str, base_url: str = "http://www.jianpu.cn") -> list[dict]:
    """Parse jianpu.cn search results page. Returns list of {title, url}."""
    soup = BeautifulSoup(html, "lxml")
    results = []
    for a in soup.find_all("a", href=re.compile(r"/pu/\d+/\d+\.htm")):
        title = a.get_text(strip=True)
        href = a.get("href", "")
        if title and href:
            url = href if href.startswith("http") else base_url + href
            results.append({"title": title, "url": url})
    return results


def parse_detail_page(html: str, base_url: str = "http://www.jianpu.cn") -> dict:
    """Parse jianpu.cn detail page. Returns {title, artist, images}."""
    soup = BeautifulSoup(html, "lxml")

    title = ""
    artist = ""
    page_title = soup.find("title")
    if page_title:
        text = page_title.get_text()
        m = re.match(r"(.+?)\s*[-–—]\s*(.+?)\s*简谱", text)
        if m:
            title = m.group(1).strip()
            artist = m.group(2).strip()
        else:
            title = text.replace("简谱", "").strip()

    images = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and any(ext in src.lower() for ext in (".jpg", ".png", ".gif")):
            if not src.startswith("http"):
                src = base_url + "/" + src.lstrip("/")
            images.append(src)

    return {"title": title, "artist": artist, "images": images[:5]}
