#!/usr/bin/python

import sys
import requests
import xml.etree.ElementTree as ET
from urllib2 import urlopen
import pycurl
from multiprocessing import Pool
from StringIO import StringIO
import argparse
from datetime import datetime
import time

startTime = datetime.now()


def curlUrl(requestUrl):
    """

    Main GET request via cURL

    :param requestUrl:
    :return:
    """

    buffer = StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, requestUrl)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    status = c.getinfo(pycurl.HTTP_CODE)
    effectiveURL = c.getinfo(pycurl.EFFECTIVE_URL)
    c.close()

    print status, effectiveURL


def loadBatchFile(file):
    """

    Load Batch file as String

    :param file:
    :return:

    """

    f = open(file)
    lines = [i.rstrip() for i in f.readlines()]

    return lines


def getSiteMap(requestUrl):
    """

    Load sitemap.xml

    :param requestUrl:
    :return:
    """

    currentUrlList = []

    try:

        # Check string
        if requestUrl.startswith('http://'):
            URL = requestUrl + "/sitemap.xml"
        elif requestUrl.startswith('https://'):
            URL = requestUrl + "/sitemap.xml"
        else:
            URL = "http://" + requestUrl + "/sitemap.xml"


        print URL

        # XML ElementTree
        tree = ET.parse(urlopen(URL))
        root = tree.getroot()
        ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Loop throught namespaced sitemap XML
        for url in root.findall('sitemap:url', ns):
            loc = url.find('sitemap:loc', ns)

            # Build fresh list
            currentUrlList.append(loc.text)

    except:

        # log error
        print "error: " + URL

    return currentUrlList



#
# Main functionality
#
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

        currentUrlList = []

        print "file = " + args.file

        # Load and parse each line of the file as URLs
        data = loadBatchFile(args.file)

        for url in data:
            currentUrlList = getSiteMap(url)

            # Map List
            p.map(curlUrl, currentUrlList)

            # Count URLs from sitemap
            count = len(currentUrlList)
            print "URL COUNT : ", count

            time.sleep(2)

    # URL STRING - Default to provided URL (full)
    else:

        print "Requesting URL : " + args.url

        URL = args.url + "/sitemap.xml"

        tree = ET.parse(urlopen(URL))
        root = tree.getroot()
        currentUrlList = []
        ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Loop throught namespaced sitemap XML
        for url in root.findall('sitemap:url', ns):
            loc = url.find('sitemap:loc', ns)

            # Build fresh list
            currentUrlList.append(loc.text)

        # Map List
        p.map(curlUrl, currentUrlList)

        # Count URLs from sitemap
        count = len(currentUrlList)
        print "URL COUNT : ", count

        print datetime.now() - startTime
