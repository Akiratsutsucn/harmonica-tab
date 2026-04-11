"""Web scraper for 2qupu.com — extracts song metadata and jianpu image URLs."""
import asyncio
import logging
import re

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
}
REQUEST_DELAY = 2.0
BASE_URL = "https://www.2qupu.com"
SEARCH_URL = f"{BASE_URL}/index.php"


async def scrape_jianpu(params: dict) -> dict:
    """Task handler: scrape 2qupu.com for harmonica sheet music."""
    query = params.get("query", "")
    max_results = min(params.get("max_results", 10), 20)

    if not query.strip():
        return {"error": "搜索关键词不能为空", "songs": [], "count": 0}

    try:
        results = await _search_and_fetch(query, max_results)
        return {
            "message": f"从 2qupu.com 搜索到 {len(results)} 首口琴谱（简谱为图片，需 OCR/LLM 提取音符）",
            "songs": results,
            "count": len(results),
        }
    except Exception as e:
        logger.exception("Scrape failed")
        return {"error": str(e), "songs": [], "count": 0}


async def _search_and_fetch(query: str, max_results: int) -> list[dict]:
    results = []
    async with httpx.AsyncClient(timeout=15, headers=HEADERS, follow_redirects=True) as client:
        try:
            resp = await client.get(SEARCH_URL, params={
                "m": "search", "c": "index", "a": "init",
                "typeid": "1", "siteid": "1", "q": query,
            })
            resp.raise_for_status()
        except httpx.HTTPError as e:
            logger.error("Search request failed: %s", e)
            return []

        soup = BeautifulSoup(resp.content, "lxml")
        links = _extract_search_links(soup, max_results)

        for item in links:
            await asyncio.sleep(REQUEST_DELAY)
            try:
                detail = await _fetch_detail(client, item["url"])
                results.append({**item, **detail})
            except Exception as e:
                logger.warning("Detail fetch failed for %s: %s", item["url"], e)
                results.append({**item, "images": [], "error": str(e)})

    return results


def _extract_search_links(soup: BeautifulSoup, max_results: int) -> list[dict]:
    """Extract harmonica-only links from search results."""
    links = []
    for a in soup.find_all("a", href=re.compile(r"/kouqin/\d{8}/\d+\.html")):
        title = re.sub(r"<[^>]+>", "", a.decode_contents()).strip()
        href = a.get("href", "")
        if not title or not href:
            continue
        url = href if href.startswith("http") else BASE_URL + href
        links.append({"title": title, "url": url})
        if len(links) >= max_results:
            break
    return links


async def _fetch_detail(client: httpx.AsyncClient, url: str) -> dict:
    resp = await client.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "lxml")

    # Extract title from h1
    h1 = soup.find("h1")
    detail_title = h1.get_text(strip=True) if h1 else ""

    # Extract sheet music images (from file.2qupu.com, skip site logos/icons)
    images = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if not src:
            continue
        if "file.2qupu.com" in src and any(ext in src.lower() for ext in (".jpg", ".png", ".gif")):
            images.append(src)

    # Try to extract artist from title tag or h1
    artist = ""
    page_title = soup.find("title")
    if page_title:
        text = page_title.get_text()
        # Format: "歌名口琴谱-口琴曲谱-爱曲谱网"
        m = re.match(r"(.+?)口琴谱", text)
        if m:
            raw = m.group(1).strip()
            # Try to split "歌名（歌手）" or "歌手：歌名"
            am = re.search(r"[（(](.+?)[）)]", raw)
            if am:
                artist = am.group(1).strip()

    return {"detail_title": detail_title, "images": images[:5], "artist": artist}
