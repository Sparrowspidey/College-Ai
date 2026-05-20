import time
from pathlib import Path
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from app.ingestion.crawler.link_manager import LinkManager
from app.ingestion.crawler.content_extractor import ContentExtractor
from app.ingestion.crawler.pdf_collector import PDFCollector


class CrawlerEngine:

    def __init__(
        self,
        start_url:   str,
        website_dir: str,
        pdf_dir:     str,
        max_pages:   int   = 200,
        delay:       float = 1.0,
    ):
        self.start_url   = start_url
        self.max_pages   = max_pages
        self.delay       = delay

        domain           = urlparse(start_url).netloc.replace("www.", "")
        self.base_domain = domain

        self.links         = LinkManager(domain)
        self.extractor     = ContentExtractor()
        self.pdf_collector = PDFCollector(pdf_dir)

        self.website_dir = Path(website_dir)
        self.website_dir.mkdir(parents=True, exist_ok=True)

        # Track which base URLs have been fully loaded in the browser
        # so we don't reload the SPA unnecessarily
        self._loaded_base: str | None = None

    # ------------------------------------------------------------------
    def crawl(self) -> None:
        print(f"\n🕷  Starting crawl: {self.start_url}")
        print(f"   Max pages : {self.max_pages}")
        print(f"   Delay     : {self.delay}s\n")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page    = browser.new_page()

            page.set_extra_http_headers({
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
            })

            count = 0

            while count < self.max_pages:
                url = self.links.next_link()
                if not url:
                    print("✅ No more links to crawl.")
                    break

                print(f"  [{count + 1}/{self.max_pages}] Crawling: {url}")

                try:
                    html = self._navigate(page, url)

                    if html is None:
                        self.links.visited.add(url)
                        count += 1
                        time.sleep(self.delay)
                        continue

                    if self._is_error_page(html):
                        print(f"    ⚠ Skipped (error/404 page)")
                        self.links.visited.add(url)
                        count += 1
                        time.sleep(self.delay)
                        continue

                    text = self.extractor.extract_text(html)

                    if text.strip():
                        self._save_page(url, text)
                    else:
                        print(f"    ⚠ Empty content, skipping save.")

                    self._extract_links_from_page(page, url)

                except Exception as e:
                    print(f"    ✗ Failed: {e}")

                self.links.visited.add(url)
                count += 1
                time.sleep(self.delay)

            browser.close()

        print(f"\n🏁 Crawl complete. Pages saved: {count}")

    # ------------------------------------------------------------------
    def _navigate(self, page, url: str) -> str | None:
        """
        Smart navigation strategy:
        - Hashbang SPA URLs (#! routes): change hash without full reload
        - Regular URLs: full page.goto()
        
        This is critical for IIIT Kottayam's Angular SPA.
        Full page reloads on hash URLs break the router and
        render wrong content (the IDY-2020 fallback view).
        """
        parsed   = urlparse(url)
        fragment = parsed.fragment  # everything after #

        is_hashbang = fragment.startswith("!")

        if is_hashbang:
            base_url = f"{parsed.scheme}://{parsed.netloc}/"

            # Load the base SPA page fresh if we're on a different domain
            if self._loaded_base != parsed.netloc:
                print(f"    → Loading SPA base: {base_url}")
                page.goto(base_url, timeout=60_000, wait_until="networkidle")
                page.wait_for_timeout(3000)
                self._loaded_base = parsed.netloc

            # Use hash change to trigger SPA routing (no full reload)
            page.evaluate(f"window.location.hash = '#{fragment}'")

            # Wait for the SPA to render the new view
            page.wait_for_timeout(3000)

        else:
            # Regular page: full navigation
            page.goto(url, timeout=60_000, wait_until="load")
            page.wait_for_timeout(2000)

            # Reset loaded base since we navigated away from the SPA
            parsed_netloc = parsed.netloc
            if self._loaded_base and self._loaded_base != parsed_netloc:
                self._loaded_base = None

        return page.content()

    # ------------------------------------------------------------------
    def _is_error_page(self, html: str) -> bool:
        error_signals = [
            "404 Not Found",
            "403 Forbidden",
            "500 Internal Server Error",
            "Page Not Found",
            "The requested URL was not found",
        ]
        html_lower = html.lower()
        return any(sig.lower() in html_lower for sig in error_signals)

    # ------------------------------------------------------------------
    def _extract_links_from_page(self, page, base_url: str) -> None:
        """Extract all rendered links via Playwright evaluate()."""
        try:
            hrefs = page.evaluate("""
                () => Array.from(document.querySelectorAll('a[href]'))
                          .map(a => a.href)
            """)
            for full_url in hrefs:
                if not full_url:
                    continue
                if full_url.lower().endswith(".pdf"):
                    self.pdf_collector.download(full_url)
                else:
                    self.links.add_link(full_url)

        except Exception as e:
            print(f"    ⚠ Link extraction failed: {e}")
            try:
                html = page.content()
                soup = BeautifulSoup(html, "html.parser")
                for tag in soup.find_all("a", href=True):
                    href = tag.get("href")
                    if not href:
                        continue
                    full_url = urljoin(base_url, href.strip())
                    if full_url.lower().endswith(".pdf"):
                        self.pdf_collector.download(full_url)
                    else:
                        self.links.add_link(full_url)
            except Exception:
                pass

    # ------------------------------------------------------------------
    def _save_page(self, url: str, text: str) -> None:
        filename = (
            url.replace("https://", "")
               .replace("http://",  "")
               .replace("/", "_")
               .replace("?", "_")
               .replace("&", "_")
               .replace("=", "_")
               .replace("#", "_")
               .replace("!", "_")
        )
        filename = filename[:180] + ".txt"
        file_path = self.website_dir / filename

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"URL: {url}\n\n")
            f.write(text)