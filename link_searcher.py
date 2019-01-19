from html.parser import HTMLParser
from urllib import parse

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = ()

    # handling
    def handle_starttag(self, tag, attrs):
        print(tag)
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    # if relative, get full domain name... does not change absolute url
                    url = parse.urljoin(self.base_url, value)
                    self.links,add(url)
    
    def page_links(self):
        return self.links

    # Will need to apply strategies to here maybe
    def error(self, message):
        pass

# finder = LinkFinder()
# finder.feed('<html><head><title>Test</title></head>'
#             '<body><h1>Parse me!</h1></body></html>')