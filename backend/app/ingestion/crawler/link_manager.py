from collections import deque
from urllib.parse import urlparse, urlunparse, urlencode, parse_qs


_SKIP_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".ico",
    ".mp4", ".mp3", ".avi", ".mov",
    ".zip", ".rar", ".tar", ".gz",
    ".exe", ".dmg", ".apk",
    ".pdf",
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".css", ".js", ".json", ".xml", ".rss",
}

_SKIP_PREFIXES = ("mailto:", "tel:", "javascript:", "whatsapp:", "sms:")

_SKIP_DOMAINS = {
    "facebook.com", "twitter.com", "instagram.com", "linkedin.com",
    "youtube.com", "t.me", "wa.me", "google.com",
}

_BLOCKED_SUBDOMAINS = {
    "opac.iiitkottayam.ac.in",   # library catalog — thousands of junk pages
    "idp.iiitkottayam.ac.in",    # SSO / login system
    "lms.iiitkottayam.ac.in",    # LMS — requires login
    "lmsug23.iiitkottayam.ac.in",
    "lmspg24.iiitkottayam.ac.in",
    "lmsone.iiitkottayam.ac.in",
}


class LinkManager:

    def __init__(self, base_domain: str):
        self.base_domain = base_domain.replace("www.", "")
        self.visited:  set[str] = set()
        self._queued:  set[str] = set()
        self._queue:   deque    = deque()

    def add_link(self, url: str) -> None:
        if any(url.startswith(p) for p in _SKIP_PREFIXES):
            return

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return

        netloc = parsed.netloc.replace("www.", "")
        if self.base_domain not in netloc:
            return

        if parsed.netloc in _BLOCKED_SUBDOMAINS:
            return

        if any(skip in netloc for skip in _SKIP_DOMAINS):
            return

        path_lower = parsed.path.lower()
        if any(path_lower.endswith(ext) for ext in _SKIP_EXTENSIONS):
            return

        normalised = self._normalise(parsed)

        if normalised not in self.visited and normalised not in self._queued:
            self._queue.append(normalised)
            self._queued.add(normalised)

    def next_link(self) -> str | None:
        while self._queue:
            url = self._queue.popleft()
            if url not in self.visited:
                return url
        return None

    @staticmethod
    def _normalise(parsed) -> str:
        sorted_query = urlencode(sorted(parse_qs(parsed.query).items()))

        fragment = parsed.fragment

        # Preserve hashbang fragments: #!/path or #!/path/subpath
        # These are real different pages in the IIITK SPA.
        # Drop regular #anchor fragments (e.g. #section-id).
        if not fragment.startswith("!"):
            fragment = ""

        clean = parsed._replace(query=sorted_query, fragment=fragment)
        url   = urlunparse(clean)

        if not fragment:
            url = url.rstrip("/")

        return url