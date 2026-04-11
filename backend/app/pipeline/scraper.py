"""Web scraper for jianpu.cn — extracts song metadata and jianpu image URLs."""
import asyncio
import logging
import re

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
REQUEST_DELAY = 2.0
BASE_URL = "http://www.jianpu.cn"


async def scrape_jianpu(params: dict) -> dict:
    """Task handler: scrape jianpu.cn for song listings."""
    query = params.get("query", "")
    max_results = min(params.get("max_results", 10), 20)

    if not query.strip():
        return {"error": "搜索关键词不能为空", "songs": [], "count": 0}

    try:
        results = await _search_and_fetch(query, max_results)
        return {
            "message": f"从 jianpu.cn 搜索到 {len(results)} 首（简谱为图片，需 OCR/LLM 提取音符）",
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
            resp = await client.get(f"{BASE_URL}/so.htm", params={"q": query})
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
    links = []
    for a in soup.find_all("a", href=re.compile(r"/pu/\d+/\d+\.htm")):
        title = a.get_text(strip=True)
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

    images = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if not src:
            continue
        if any(ext in src.lower() for ext in (".jpg", ".png", ".gif")):
            if not src.startswith("http"):
                src = BASE_URL + "/" + src.lstrip("/")
            images.append(src)

    artist = ""
    page_title = soup.find("title")
    if page_title:
        text = page_title.get_text()
        m = re.search(r"[-–—]\s*(.+?)\s*简谱", text)
        if m:
            artist = m.group(1).strip()

    return {"images": images[:5], "artist": artist}
