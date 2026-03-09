from app.ingestion.crawler.crawler_engine import CrawlerEngine


def run_crawler():

    crawler = CrawlerEngine(

        start_url="https://www.iiitkottayam.ac.in",

        website_dir="data/raw/website",

        pdf_dir="data/raw/pdf",

        max_pages=200

    )

    crawler.crawl()