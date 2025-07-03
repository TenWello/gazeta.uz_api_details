import requests
from bs4 import BeautifulSoup
import re

def get_gazeta_uz_latest_links(limit: int = 30):
    url = "https://www.gazeta.uz/oz/"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "uz,ru;q=0.9,en;q=0.8",
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    links = []

    for a in soup.select(".latest-news__item a[href^='/oz/']"):
        full = "https://www.gazeta.uz" + a["href"]
        if full not in links:
            links.append(full)

    for a in soup.select("a.news-card__title[href^='/oz/']"):
        full = "https://www.gazeta.uz" + a["href"]
        if full not in links:
            links.append(full)

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/oz/20") and len(href.split("/")) >= 6:
            full = "https://www.gazeta.uz" + href
            if full not in links:
                links.append(full)

    return links[:limit]

def get_gazeta_uz_details(link: str) -> dict:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(link, headers=headers, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    title_tag = soup.find("h1", id="article_title") or soup.find("h1", id="article-title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    time_ago = ""
    dt = soup.find("div", class_="articleDateTime")
    if dt:
        for node in dt.find_all(string=True, recursive=False):
            txt = node.strip()
            if re.match(r"^(Bugun|Kecha|\d{4}-yil)", txt):
                time_ago = txt
                break

    body = (
        soup.select_one(".js-mediator-article.article-text")
        or soup.select_one(".redactor-js-mediator-article.article-text")
        or soup.select_one(".article-text")
    )
    full_text = ""
    if body:
        paras = [p.get_text(strip=True) for p in body.find_all("p")]
        full_text = "\n".join(paras)

    images = []
    main = soup.find("img", class_="articleBigPic")
    if main and main.get("src"):
        images.append(main["src"])
    if body:
        for img in body.find_all("img"):
            src = img.get("src")
            if src and src not in images:
                images.append(src)

    return {
        "title":     title,
        "link":      link,
        "time_ago":  time_ago,
        "full_text": full_text,
        "images":    images,
    }
