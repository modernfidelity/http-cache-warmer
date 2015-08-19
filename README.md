HTTP Cache Warmer
=================

 Simple scripts to loop over a selection of site URLs that are running Google Sitemap XML, parse the returns and then call cURL GET requests to the endpoints, in turn 'warming' (generating) caches.

## Install 

Clone the repo and then run the following CLI commands.


### PHP (5.5+)

```
php warmer.php http://www.your-website-running-google-sitemap-xml.com

```

### Python (2.7.x)

Run against a single URL/website :

```
python warmer.py --url http://www.your-website-running-google-sitemap-xml.com

```

Run a batch file containg a list of URLs/websites :

```
python warmer.py --file batchurls.txt

```

The scripts will add /sitemap.xml to the end of the URL, then perform GET requests on each of the return sitemap URLs.
 
### @TODO : 
 
  - Add batch functionality from file.
  - Better memory + file processing for large maps.
