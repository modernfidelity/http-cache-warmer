HTTP Cache Warmer
=================

 Simple scripts to loop over a selection of site URLs that are running Google Sitemap XML, parse the returns and then call cURL GET requests to the endpoints, in turn 'warming' (generating) caches.

## Install 

Clone the repo and then run the following CLI commands.


### PHP

```
php warmer.php http://www.your-website-running-google-sitemap-xml.com

```

### PYTHON

```
python warmer.py http://www.your-website-running-google-sitemap-xml.com

```

The scripts will add /sitemap.xml to the end of the URL, then perform GET requests on each of the return sitemap URLs.
 
### @TODO : 
 
  - Add batch functionality from file.
  - Better memory + file processing for large maps.
