import logging
import xml.etree.ElementTree as Et
from urllib2 import urlopen
import pycurl
from multiprocessing import Pool
from StringIO import StringIO
import argparse
from datetime import datetime

startTime = datetime.now()


def curlurl(requesturl):
    """
    Main GET request via cURL
    :param requesturl:
    :return:
    """

    writebuffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, requesturl)
    c.setopt(c.WRITEDATA, writebuffer)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.CONNECTTIMEOUT, 5)
    c.setopt(c.TIMEOUT, 10)
    # c.setopt(c.VERBOSE, True)
    c.setopt(c.FAILONERROR, False)

    try:
        c.perform()
        status = c.getinfo(pycurl.HTTP_CODE)
        effectiveurl = c.getinfo(pycurl.EFFECTIVE_URL)
        c.close()

        if status:
            print status, effectiveurl

    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr


def loadbatchfile(batchfile):
    """
    Load Batch file as String
    :param batchfile:
    :return:
    """

    f = open(batchfile)
    lines = [i.rstrip() for i in f.readlines()]
    return lines


def getsitemap(requesturl):
    """
    Load sitemap.xml
    :param requesturl:
    :return:
    """
    
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

        # Loop through namespace sitemap XML
        for url in root.findall('sitemap:url', ns):
            loc = url.find('sitemap:loc', ns)
            # Build fresh list
            currenturllist.append(loc.text)

        return currenturllist

    except IOError as e:

        # log error
        print "error: " + format(e.errno, e.strerror)

# Main functionality
if __name__ == '__main__':

    logging.info("log message")

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
            # time.sleep(0.5)

    # URL STRING - Default to provided URL (full)
    else:

        print "Requesting URL : " + args.url
        URL = args.url + "/sitemap.xml"
        tree = Et.parse(urlopen(URL))
        root = tree.getroot()
        currenturllist = []
        ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Loop through namespace sitemap XML
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
