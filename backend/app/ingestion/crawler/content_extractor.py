import re
from bs4 import BeautifulSoup


class ContentExtractor:

    # UI artifact words to throw away (exact line match)
    NOISE_WORDS = {
        "more_vert", "close", "×", "Visit Gallery",
        "Congratulations", "Click Here", "Read More", "Back to Top",
    }

    # Only match clearly structural/UI class names — NOT broad words
    # that might accidentally match content divs (e.g. "header", "banner")
    NOISE_CLASS_PATTERNS = re.compile(
        r"\bnav(bar|igation)?\b"   # navbar, navigation, nav
        r"|\bsidebar\b"
        r"|\bbreadcrumb\b"
        r"|\bcookie(-banner)?\b"
        r"|\bpopup\b"
        r"|\bmodal\b"
        r"|\boverlay\b"
        r"|\bdropdown(-menu)?\b"
        r"|\btopbar\b"
        r"|\bmega-?menu\b",
        re.IGNORECASE,
    )

    def extract_text(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        # Remove clearly non-content tags
        for tag in soup(
            ["script", "style", "nav", "footer",
             "button", "form", "svg", "noscript", "iframe"]
        ):
            tag.decompose()

        # Collect tags to remove first, then decompose (avoids tree mutation bug)
        tags_to_remove = []
        for tag in soup.find_all(True):
            try:
                classes = " ".join(tag.get("class") or [])
                tag_id  = tag.get("id") or ""
                if self.NOISE_CLASS_PATTERNS.search(classes) or \
                   self.NOISE_CLASS_PATTERNS.search(tag_id):
                    tags_to_remove.append(tag)
            except Exception:
                continue

        for tag in tags_to_remove:
            tag.decompose()

        raw_text = soup.get_text(separator="\n")
        lines    = self._clean_lines(raw_text)

        return "\n".join(lines)

    # ------------------------------------------------------------------
    def _clean_lines(self, raw_text: str) -> list[str]:
        seen   = set()
        result = []

        for line in raw_text.splitlines():
            line = line.strip()

            # Drop empty or very short lines
            if len(line) < 4:
                continue

            # Drop known noise words (exact match)
            if line in self.NOISE_WORDS:
                continue

            # Drop lines with no alphanumeric characters
            if not re.search(r"[a-zA-Z0-9]", line):
                continue

            # Deduplicate
            if line in seen:
                continue

            seen.add(line)
            result.append(line)

        return result