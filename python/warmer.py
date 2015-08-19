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

    # return c.getinfo(pycurl.HTTP_CODE), c.getinfo(pycurl.EFFECTIVE_URL)
    # return buffer.getvalue()




def loadBatchFile(file):

    """
    Load a batch of URLs from a file

    :param file:
    :return:
    """
    return open(file)


def getSiteXml(requestUrl):
    return

def getUrl(url):
    return

def parseXml(url):
    return


#
# Main functionality
#
if __name__ == '__main__':



    # Add CLI helpers
    parser = argparse.ArgumentParser(
        description='HTTP CACHE WARMER :: Lets warm things up a bit...'
    )

    parser.add_argument('--url', help='The URL to test')

    parser.add_argument('--file', help='The batch file of URLs to process')

    args = parser.parse_args()


    # Setup Multiprocessing

    p = Pool(64)


    # Check for Batch file
    if args.file:


        print "@todo - file = " + args.file



    # Default to provided URL (full)
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
            # GET Request each URL
            # curlUrl(loc.text)


        # Map List
        p.map(curlUrl, currentUrlList)

        # Count URLs from sitemap
        count = len(currentUrlList)
        print "URL COUNT : ", count

        print datetime.now() - startTime
