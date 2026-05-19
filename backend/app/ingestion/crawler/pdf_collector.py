import requests
from pathlib import Path
from urllib.parse import urlparse


# PDFs larger than this will be skipped (bytes) — 50 MB
MAX_PDF_SIZE = 50 * 1024 * 1024

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; CollegeAI-Crawler/1.0; "
        "+https://github.com/Sparrowspidey/College-Ai)"
    )
}


class PDFCollector:

    def __init__(self, save_dir: str):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.downloaded: set[str] = set()

    # ------------------------------------------------------------------
    def download(self, url: str) -> None:
        filename = self._safe_filename(url)
        path     = self.save_dir / filename

        if path.exists() or url in self.downloaded:
            return

        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=30,
                stream=True,          # stream so we can check size
            )

            if response.status_code != 200:
                print(f"  ✗ PDF skipped (HTTP {response.status_code}): {url}")
                return

            # Verify it is actually a PDF by content-type
            content_type = response.headers.get("Content-Type", "")
            if "pdf" not in content_type.lower():
                print(f"  ✗ Not a PDF (Content-Type: {content_type}): {url}")
                return

            # Check size before writing
            content_length = int(response.headers.get("Content-Length", 0))
            if content_length > MAX_PDF_SIZE:
                print(f"  ✗ PDF too large ({content_length / 1e6:.1f} MB): {url}")
                return

            # Write in chunks to avoid loading huge files into RAM
            with open(path, "wb") as f:
                size = 0
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    size += len(chunk)
                    if size > MAX_PDF_SIZE:
                        print(f"  ✗ PDF exceeded size limit mid-download: {url}")
                        path.unlink(missing_ok=True)
                        return

            self.downloaded.add(url)
            print(f"  ✓ PDF saved ({size / 1024:.0f} KB): {filename}")

        except requests.exceptions.Timeout:
            print(f"  ✗ PDF download timed out: {url}")
        except requests.exceptions.RequestException as e:
            print(f"  ✗ PDF download failed: {url} → {e}")

    # ------------------------------------------------------------------
    @staticmethod
    def _safe_filename(url: str) -> str:
        """Derive a clean filename from the URL path."""
        path = urlparse(url).path
        name = path.split("/")[-1] or "download"
        # Replace characters that are invalid in filenames
        for ch in r'\/:*?"<>|':
            name = name.replace(ch, "_")
        if not name.lower().endswith(".pdf"):
            name += ".pdf"
        return name