import advertools
import requests

from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache
from bs4 import BeautifulSoup

#Change to your site and sitemap url e.g. siteMapUrl = "https://talotics.com/sitemap.xml"
siteMapUrl = "https://mysite.com/my-sitemap-posts-url.xml"
sitemapDataFrame = advertools.sitemap_to_df(siteMapUrl, recursive=True)

forever_cache = FileCache('.web_cache', forever=True)
session = CacheControl(requests.Session(), forever_cache)

urls = sitemapDataFrame['loc'].tolist()

for url in urls:
    urlReport = []
    print(url)
    html = session.get(url).text
    
    parsedHtml = BeautifulSoup(html, 'html.parser')
    iframes = parsedHtml.find_all('iframe')
    
    for iframe in iframes:
        lazy = iframe.get('loading')
        if(lazy==None or lazy!="lazy"):
            print("")
            print(iframe)
            print("- has an iframe without lazy loading")

    elements = parsedHtml.find_all('img')
    
    for element in elements:
        attribute = element.get('alt')
        if(attribute==None or attribute==""):
            print("")
            print(element)
            print("- has no alt")