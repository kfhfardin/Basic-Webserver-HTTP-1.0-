<html>
<!-- WHAT FOLLOWS IS HTML AND PHP CODE. IF THE CODE IS BEING DISPLAYED IN YOUR BROWSER, YOU DID NOT GET PHP WORKING YET... -->
 <head>
  <title>PHP Test for CGI Query String</title>
 </head>
 <body>
<H1> Test Results (if nothing appears, PHP is not working):</H1>
<?php
if (isset($_GET["get_test1"]) and $_GET["get_test1"]=="test1 pass" and isset($_GET["get_test2"]) and $_GET["get_test2"]=="test2 pass") {
   echo "QUERY STRING TEST PASSED! Note this does not mean your CGI works perfectly according to the CGI/1.1 spec, but it at least passed the test.";
}
else {
   echo "QUERY STRING TEST FAILED! Your CGI is not working correctly.";
}

?> 
 </body>
</html>