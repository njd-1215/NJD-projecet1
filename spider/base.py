import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class BaseSpider:
    """招投标网站爬虫基础类"""

    def __init__(self, site_config):
        self.cfg = site_config
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def fetch_list(self):
        """抓取列表页，返回标准化的项目列表"""
        resp = self.session.get(self.cfg["url"], timeout=30)
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, "lxml")

        items = []
        for row in soup.select(self.cfg["list_selector"]):
            title_el = row.select_one(self.cfg["title_selector"])
            if not title_el:
                continue

            title = title_el.get_text(strip=True)
            link = urljoin(self.cfg["url"], title_el.get("href", ""))

            date_el = row.select_one(self.cfg.get("date_selector", ""))
            date = date_el.get_text(strip=True) if date_el else ""

            items.append({
                "site": self.cfg["name"],
                "title": title,
                "url": link,
                "date": date,
            })

        return items
