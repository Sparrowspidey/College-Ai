from urllib.parse import urlparse

class LinkManager:

    def __init__(self, base_domain):
        self.base_domain = base_domain
        self.visited = set()
        self.queue = []

    def add_link(self, url):
        parsed = urlparse(url)
        if self.base_domain not in parsed.netloc:
            return

        clean_url = url.split('#')[0]

        if clean_url not in self.visited and clean_url not in self.queue:
            self.queue.append(clean_url)

    def next_link(self):
        if self.queue:
            return self.queue.pop(0)
        return None             
