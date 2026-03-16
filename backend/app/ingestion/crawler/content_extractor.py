from bs4 import BeautifulSoup


class ContentExtractor:

    def extract_text(self, html):
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator = "\n")

        lines = [line.strip() for line in text.splitlines() if line.strip()]

        return "\n".join(lines)
    
        