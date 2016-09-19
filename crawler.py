import time, sys
from datetime import timedelta

try:
    from HTMLParser import HTMLParser
    from urlparse import urljoin, urldefrag
except ImportError:
    from html.parser import HTMLParser
    from urllib.parse import urljoin, urldefrag

from tornado import httpclient, gen, ioloop, queues

concurrency = 10

# base url is given as an input when running the program
base_url = sys.argv[1]

@gen.coroutine
def get_links_from_url(url):
    try:
        response = yield httpclient.AsyncHTTPClient().fetch(url)
        print(url)

        html = response.body if isinstance(response.body, str) \
            else response.body.decode()
        urls = [urljoin(url, remove_fragment(new_url))
                for new_url in get_links(html)]
    except Exception as e:
        print('Exception: %s %s' % (e, url))
        raise gen.Return([])

    raise gen.Return(urls)


def remove_fragment(url):
    pure_url, frag = urldefrag(url)
    return pure_url


def get_links(html):
    class URLSeeker(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.urls = []

        def handle_starttag(self, tag, attrs):
            href = dict(attrs).get('href')
            if href and tag == 'a':
                self.urls.append(href)

    url_seeker = URLSeeker()
    url_seeker.feed(html)
    return url_seeker.urls

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

@gen.coroutine
def main():

    file = open("raw_extracted.txt", 'a') # mode a for last line
    q = queues.Queue()
    start = time.time()
    fetching, fetched = set(), set()

    @gen.coroutine
    def fetch_url():
        current_url = yield q.get()
        try:
            if current_url in fetching:
                return
            if(is_ascii(current_url)):
                fetching.add(current_url)
                if ('/answ' in current_url) and not('/profile/' in current_url):
                    current_url, unwanted = current_url.split('/ans')
                    file.write(current_url + '\n')
                    time.sleep(0.1)
                urls = yield get_links_from_url(current_url)
                if not('sitemap' in current_url):
                    fetched.add(current_url)
                    for new_url in urls:
                        if new_url.startswith('https://www.quora.com/'):
                            yield q.put(new_url)
        finally:
            q.task_done()

    @gen.coroutine
    def worker():
        while True:
            yield fetch_url()

    q.put(base_url)

    #worker initialization
    for _ in range(concurrency):
        worker()
    yield q.join(timeout=timedelta(seconds=180)) ## 3 minutes
    file.close()
    assert fetching == fetched


if __name__ == '__main__':
    import logging
    logging.basicConfig()
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)
