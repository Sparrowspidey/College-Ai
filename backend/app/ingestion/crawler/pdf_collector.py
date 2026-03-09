import requests
from pathlib import Path


class PDFCollector:

    def __init__(self, save_dir):

        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def download(self, url):

        filename = url.split("/")[-1]

        path = self.save_dir / filename

        if path.exists():
            return

        try:

            r = requests.get(url, timeout=20)

            if r.status_code == 200:

                with open(path, "wb") as f:
                    f.write(r.content)

                print("PDF saved:", filename)

        except:
            pass