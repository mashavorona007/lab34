"""

scraper.py

Implementations for URL scraping routines.

"""

from __future__ import unicode_literals

try:
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3 compatibility
    from html.parser import HTMLParser

import requests
from PIL import ImageFile

__all__ = (
    'get_thumbnail_urls',
)

BASE_HEADERS = {
    'User-Agent'    :   'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:51.0) '
                        'Gecko/20100101 Firefox/51.0',
}


class _ImageScraper(HTMLParser, object):
    """ HTMLParser subclass that scrapes image URLs from a given URL. """
    
    def __init__(self):
        super(_ImageScraper, self).__init__()
        
        self._urls = []
        
    def handle_starttag(self, tag, attrs):
        src = None
        
        if tag == 'meta':
            attrDict = dict(attrs)
            
            try:
                if attrDict['property'] == 'og:image':
                    src = attrDict['content']
            except KeyError:
                pass
                
        elif tag == 'link':
            attrDict = dict(attrs)
            
            try:
                if attrDict['rel'] == 'image_src':
                    src = attrDict['href']
            except KeyError:
                pass
                
        elif tag == 'img':
            try:
                src = dict(attrs)['src']
            except KeyError:
                pass
                
        if src is not None:
            if src.startswith('http://') or src.startswith('https://'):
                self._urls.append(src)
                
    def get_urls(self):
        return self._urls[:]
        
        
def image_size(response):
    """ Given a streaming HTTP response that gives image data, determines the 
    size of the given image data.
    
    """
    
    parser = ImageFile.Parser()
    
    while not parser.image:
        parser.feed(response.raw.read(1024))
        
    return parser.image.size
    
    
def urls_from_text(text):
    """ Given some text, returns a list of all "URL-like" strings in the text.
    
    Assumes that the text is generally composed of words that are delimited by 
    whitespace.
    
    """
    
    results = []
    for token in text.split():
        if token.startswith('http://') or token.startswith('https://'):
            results.append(token)
            
    return results
    
    
def get_thumbnail_urls(url):
    """ Takes a URL, and returns a list of URLs corresponding to possible 
    thumbnails on that page.
    
    """
    
    try:
        response = requests.get(url, timeout=5, headers=BASE_HEADERS)
    except requests.RequestException:
        return []       # Can't connect ==> no results
        
    if response.status_code != 200:
        return []       # Non-OK response ==> no results
        
    contentType = response.headers['Content-Type']
    
    if 'image' in contentType:
        return [url]    # URLs to images are their own thumbnail.
        
        
    ################################
    # Get list of URLs on the page #
    ################################
    
    if 'text/html' in contentType:
        imageScraper = _ImageScraper()
        imageScraper.feed(response.content.decode(response.encoding))
        
        urls = imageScraper.get_urls()
        
    elif 'text' in contentType:
        # Non-HTML text pages. We assume that they're probably plain text or 
        # something similar. If not, then oh well.
        
        urls = urls_from_text(response.content.decode(response.encoding))
        
    else:
        # Non-HTML, probably binary content. No thumbnails available.
        return []
        
    # List of (area, URL) tuples representing what we think are probably the 
    # main images.
    images = []
    
    # Use Black Magic to figure out which URLs are probably the main images.
    for url in urls:
        # Ignore all URLs that have the word 'sprite' in them.
        if 'sprite' in url:
            continue
            
        try:
            response = requests.get(
                url,
                timeout=10,
                headers=BASE_HEADERS,
                stream=True,
            )
        except requests.RequestException:
            continue    # Ignore bad URLs
            
        # Must actually be an image.
        if 'image' not in response.headers['Content-Type']:
            continue
            
        # Get the dimensions of the image.
        width, height = image_size(response)
        
        # Images too wide or long should be rejected.
        if not (0.5 <= float(width) / float(height) <= 2.0):
            continue
            
        area = width * height
        
        images.append((area, url))
        
    # Sort by greatest to smallest area.
    images.sort(reverse=True)
    
    # Return up to the first five biggest images.
    return [url for area, url in images[:5]]
    
    