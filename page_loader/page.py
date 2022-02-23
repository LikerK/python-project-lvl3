from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import logging


logger = logging.getLogger(__name__)


class Page(BeautifulSoup):
    TAGS_FOR_LINKS = {'img': 'src', 'link': 'href', 'script': 'src'}

    def __init__(self, url, content):
        self.url = url
        self.parsed = urlparse(self.url)
        super().__init__(content, "html.parser")
        self.local_links_url = self._get_links_to_local_files()

    def _is_link_to_local_file(self, path):
        url = urlparse(path)
        if url.scheme and url.netloc != self.parsed.netloc:
            return False
        return True

    def _get_links_to_local_files(self):
        old_links = dict()
        for tag in self.find_all():
            if tag.name in self.TAGS_FOR_LINKS:
                attr = tag.get(self.TAGS_FOR_LINKS[tag.name])
                if not attr:
                    continue
                if self._is_link_to_local_file(attr):
                    domain_link = urljoin(self.url, attr)
                    logger.debug(f'get domain link from {attr}')
                    previous_items = old_links.setdefault(domain_link, [])
                    previous_items.append(tag)
                    old_links[domain_link] = previous_items
        logger.debug(f'extracted {len(old_links)} domain names')
        return old_links

    @property
    def get_domain_links(self):
        return self.local_links_url.keys()

    def replace_links(self, new_links):
        logger.debug(f'started to rename {len(new_links)} html domain names')
        for old_link, new_link in new_links.items():
            tags = self.local_links_url[old_link]
            for tag in tags:
                attr = self.TAGS_FOR_LINKS[tag.name]
                tag[attr] = new_link
            logger.debug(f'{old_link} changed to {new_link}')

    @property
    def html(self):
        return self.prettify()
