import logging
import xml.etree.ElementTree as Et
from urllib2 import urlopen
import pycurl
from multiprocessing import Pool
from StringIO import StringIO
import argparse
from datetime import datetime
import time

startTime = datetime.now()


def curlurl(requesturl):
    """

    Main GET request via cURL

    :param requesturl:
    :return:
    """

    buffer = StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, requesturl)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    status = c.getinfo(pycurl.HTTP_CODE)
    effectiveurl = c.getinfo(pycurl.EFFECTIVE_URL)
    c.close()

    print status, effectiveurl


def loadbatchfile(file):
    """

    Load Batch file as String

    :param file:
    :return:

    """

    f = open(file)
    lines = [i.rstrip() for i in f.readlines()]

    return lines


def getsitemap(requesturl):
    """

    Load sitemap.xml

    :param requesturl:
    :return:
    """

    currenturllist = []

    try:

        # Check string
        if requesturl.startswith('http://'):
            url = requesturl + "/sitemap.xml"
        elif requesturl.startswith('https://'):
            url = requesturl + "/sitemap.xml"
        else:
            url = "http://" + requesturl + "/sitemap.xml"

        print url

        # XML ElementTree
        tree = Et.parse(urlopen(url))
        root = tree.getroot()
        ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Loop through namespaced sitemap XML
        for url in root.findall('sitemap:url', ns):
            loc = url.find('sitemap:loc', ns)

            # Build fresh list
            currenturllist.append(loc.text)

    except:

        # log error
        print "error: " + url

    return currenturllist


# Main functionality
if __name__ == '__main__':

    # Add CLI helpers
    parser = argparse.ArgumentParser(description='HTTP CACHE WARMER :: Lets warm things up a bit...')
    parser.add_argument('--url', help='The URL to test')
    parser.add_argument('--file', help='The batch file of URLs to process')
    args = parser.parse_args()

    # Setup Multiprocessing
    p = Pool(64)

    # FILE - Check for Batch file
    if args.file:

        currenturllist = []

        print "file = " + args.file

        # Load and parse each line of the file as URLs
        data = loadbatchfile(args.file)

        for url in data:
            currenturllist = getsitemap(url)

            # Map List
            p.map(curlurl, currenturllist)

            # Count URLs from sitemap
            count = len(currenturllist)
            print "URL COUNT : ", count

            time.sleep(2)

    # URL STRING - Default to provided URL (full)
    else:

        print "Requesting URL : " + args.url

        URL = args.url + "/sitemap.xml"

        tree = Et.parse(urlopen(URL))
        root = tree.getroot()
        currenturllist = []
        ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Loop through namespaced sitemap XML
        for url in root.findall('sitemap:url', ns):
            loc = url.find('sitemap:loc', ns)

            # Build fresh list
            currenturllist.append(loc.text)

        # Map List
        p.map(curlurl, currenturllist)

        # Count URLs from sitemap
        count = len(currenturllist)
        print "URL COUNT : ", count

        print datetime.now() - startTime
