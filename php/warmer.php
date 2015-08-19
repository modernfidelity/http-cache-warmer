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


  //Get the resulting HTTP status code from the cURL handle.
  $http_status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);

  curl_close($ch);


  echo $http_status_code . " - " . $url .  "\n\r";




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

//  var_dump($xml);

  // Add counter
  $count = 1;

  // Loop through each returned URL and fire GET request.
  foreach ($xml->url as $url_list) {

    $url = $url_list->loc;

    // Output
//    echo $url . "\n\r";

    // Make a REQUEST
    getURL($url);

    // Increment count
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