#!/usr/bin/python

import sys
import requests
import xml.etree.ElementTree as ET
from urllib2 import urlopen
import pycurl
from multiprocessing import Pool
from StringIO import StringIO
import argparse


#
# Main GET request via cURL
#
def curlUrl(requestUrl):
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


#
# Load a batch of URLs from a file
#

def loadBatchFile(file):
    return open(file)


#
#
def getSiteXml(requestUrl):
    return


#
#
def getUrl(url):
    return


#
#
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

    # Check for Batch file
    if args.file:


        print "@todo - file = " + args.file



    # Default to provided URL (full)
    else:

        print "Requesting URL : " + args.url

        URL = args.url + "/sitemap.xml"

        tree = ET.parse(urlopen(URL))

        root = tree.getroot()

        ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        #
        for url in root.findall('sitemap:url', ns):
            loc = url.find('sitemap:loc', ns)

            curlUrl(loc.text)


            # -------------------------

            # website = sys.argv[1]
            #
            # URL = website + "/sitemap.xml"
            #
            # print URL
            #
