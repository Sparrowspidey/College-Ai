from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from app.ingestion.crawler.link_manager import LinkManager
from app.ingestion.crawler.content_extractor import ContentExtractor
from app.ingestion.crawler.pdf_collector import PDFCollector


class CrawlerEngine:

    def __init__(self, start_url, website_dir, pdf_dir, max_pages=200):

        self.start_url = start_url
        self.max_pages = max_pages

        domain = start_url.split("/")[2]

        self.links = LinkManager(domain)
        self.links.add_link(start_url)

        self.extractor = ContentExtractor()
        self.pdf_collector = PDFCollector(pdf_dir)

        self.website_dir = Path(website_dir)
        self.website_dir.mkdir(parents=True, exist_ok=True)

    def crawl(self):

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            count = 0

            while count < self.max_pages:

                url = self.links.next_link()

                if not url:
                    break

                if url in self.links.visited:
                    continue

                print("Crawling:", url)

                try:

                    page.goto(url, timeout=60000)

                    html = page.content()

                    text = self.extractor.extract_text(html)

                    self.save_page(url, text)

                    self.extract_links(html, url)

                except:
                    pass

                self.links.visited.add(url)

                count += 1

            browser.close()

    def extract_links(self, html, base_url):

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup.find_all("a", href=True):

            href = tag["href"]

            full_url = urljoin(base_url, href)

            if full_url.endswith(".pdf"):
                self.pdf_collector.download(full_url)
            else:
                self.links.add_link(full_url)

    def save_page(self, url, text):

        filename = url.replace("https://", "").replace("/", "_")

        file_path = self.website_dir / f"{filename}.txt"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"URL: {url}\n\n")
            f.write(text)