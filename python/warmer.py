#!/usr/bin/python

import sys
import requests
import xml.etree.ElementTree as ET
from urllib2 import urlopen
import pycurl
from multiprocessing import Pool
from StringIO import StringIO



#
#
def curlUrl(requestUrl):
    buffer = StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, requestUrl)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    return buffer.getvalue()


#
#
def getSiteXml(requestUrl):
    requestUrl = requestUrl + "/sitemap.xml"

    r = requests.get(requestUrl)

    data = r.text

    soup = BeautifulSoup(data, 'html.parser')

    collection = soup.findAll("loc")

    return collection


#
#
def getUrl(url):
    return curlUrl(url)


#
#
def parseXml(url):
    url = url + "/sitemap.xml"

    r = requests.get(url)

    data = r.text

    tree = ET.parse(data)

    root = tree.getroot()

    collection = []

    for loc in root.findAll("loc"):
        collection.append(loc.text)

        # return collection


if __name__ == '__main__':

    website = sys.argv[1]

    URL = website + "/sitemap.xml"

    print URL

    tree = ET.parse(urlopen(URL))

    root = tree.getroot()

    ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    for url in root.findall('sitemap:url', ns):
        loc = url.find('sitemap:loc', ns)
        print loc.text
