<?php


/***
 *
 *  HTTP CACHE WARMER
 *
 * Simple script to loop over a selection of URLs that are running Google Sitemap XML, parse the returns
 * and then call cURL GET request to the endpoints, in turn 'warming' (generating) caches.
 *
 *
 */

$ver = "HTTP Cache Warmer 0.1";

echo $ver . "\n\r";

// Load Map
loadSiteMapXML($argv[1]);


/**
 *
 * Make a GET request to URL via cURL
 *
 * @param $url
 */
function getURL($url) {
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  $data = curl_exec($ch);
  curl_close($ch);

}


/**
 *
 * Load Sitemap XML via cURL
 *
 * @param $url
 */
function loadSiteMapXML($url) {


  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $url . '/sitemap.xml');
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  $data = curl_exec($ch);
  curl_close($ch);


  // Break out
  parseXml($data);

}


/**
 *
 * Parse returned XML from Map
 *
 */
function parseXml($data) {

  // Break out
  $xml = new SimpleXMLElement($data);

  var_dump($xml);


  $count = 1;

  foreach ($xml->url as $url_list) {
    $url = $url_list->loc;

    echo $url . "\n\r";


    $count++;
  }

  echo "\n\r Total : " . $count . "\n\r";

}

/**
 *
 * Output returned XML data to file
 *
 * @param $data
 */
function writeFile($data, $fileName) {

  if (@simplexml_load_string($xml)) {
    $fp = fopen($fileName, 'w');
    fwrite($fp, $xml);
    fclose($fp);
  }


}