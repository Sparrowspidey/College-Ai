from app.ingestion.crawler.crawler_engine import CrawlerEngine


# -----------------------------------------------------------------------
# All URLs confirmed directly from the IIIT Kottayam website navigation.
# The site uses hashbang SPA routing: https://www.iiitkottayam.ac.in/#!/page
# -----------------------------------------------------------------------

MAIN = "https://www.iiitkottayam.ac.in"

SEED_URLS = [

    # ── General ─────────────────────────────────────────────────────────
    f"{MAIN}/#!/home",
    f"{MAIN}/#!/whyIIITK",
    f"{MAIN}/#!/nirf_home",
    f"{MAIN}/#!/institute",
    f"{MAIN}/#!/admission",
    f"{MAIN}/#!/academics",
    f"{MAIN}/#!/scholarship",

    # ── B.Tech Courses ──────────────────────────────────────────────────
    f"{MAIN}/#!/btech_cs_home",
    f"{MAIN}/#!/btech_ec_home",
    f"{MAIN}/#!/btech_cyber_home",
    f"{MAIN}/#!/btech_ai_home",

    # ── People ──────────────────────────────────────────────────────────
    f"{MAIN}/#!/admin",
    f"{MAIN}/#!/dept_head",
    f"{MAIN}/#!/faculty",
    f"{MAIN}/#!/technical",
    f"{MAIN}/#!/professional",
    f"{MAIN}/#!/researchScholar",

    # ── Students ────────────────────────────────────────────────────────
    f"{MAIN}/#!/students/batch15",
    f"{MAIN}/#!/executivemtech/mtech_batch25",
    f"{MAIN}/#!/imtechStudents/imtech_batch26",
    f"{MAIN}/#!/emtechStudents/emtech_batch26",

    # ── Campus / Facilities ─────────────────────────────────────────────
    f"{MAIN}/#!/campus/overview",
    f"{MAIN}/#!/campus/hostel",
    f"{MAIN}/#!/campus/security",
    f"{MAIN}/#!/campus/internet",
    f"{MAIN}/#!/campus/gymnasium",
    f"{MAIN}/#!/campus/sports",
    f"{MAIN}/#!/campus/atm",
    f"{MAIN}/#!/campus/medical",
    f"{MAIN}/#!/studMess",

    # ── Events & Activities ─────────────────────────────────────────────
    f"{MAIN}/#!/innovations",
    f"{MAIN}/#!/fdp_webinar",
    f"{MAIN}/#!/events",

    # ── Clubs ───────────────────────────────────────────────────────────
    f"{MAIN}/#!/culturalClub",
    f"{MAIN}/#!/codingClub",
    f"{MAIN}/#!/sportsClub",
    f"{MAIN}/#!/socialClub",
    f"{MAIN}/#!/cybersecurityClub",
    f"{MAIN}/#!/mindquest",
    f"{MAIN}/#!/magazine",
    f"{MAIN}/#!/ieee",
    f"{MAIN}/#!/acm",

    # ── Research ────────────────────────────────────────────────────────
    f"{MAIN}/#!/researchPublication",
    f"{MAIN}/#!/researchGroups",
    f"{MAIN}/#!/studentPublication",
    f"{MAIN}/#!/researchProject",
    f"{MAIN}/#!/awards",
    f"{MAIN}/#!/collaboration",
    f"{MAIN}/#!/researchActivities",

    # ── Placement & Media ───────────────────────────────────────────────
    f"{MAIN}/#!/placement",
    f"{MAIN}/#!/media",

    # ── Subdomains ──────────────────────────────────────────────────────
    "https://emtech.iiitkottayam.ac.in",
    "https://mtech.iiitkottayam.ac.in",
    "https://imtech.iiitkottayam.ac.in",
    "https://phd.iiitkottayam.ac.in",
    "https://icentre.iiitkottayam.ac.in",
]


def run_crawler(
    website_dir: str   = "../data/raw/website",
    pdf_dir:     str   = "../data/raw/pdf",
    max_pages:   int   = 300,
    delay:       float = 1.5,
) -> None:
    crawler = CrawlerEngine(
        start_url   = MAIN,
        website_dir = website_dir,
        pdf_dir     = pdf_dir,
        max_pages   = max_pages,
        delay       = delay,
    )

    for url in SEED_URLS:
        crawler.links.add_link(url)

    crawler.crawl()