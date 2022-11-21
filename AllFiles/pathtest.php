<html>
<!-- WHAT FOLLOWS IS HTML AND PHP CODE. IF THE CODE IS BEING DISPLAYED IN YOUR BROWSER, YOU DID NOT GET PHP WORKING YET... -->
 <head>
  <title>PHP Test for correct handling of extended paths</title>
 </head>
 <body>
<H1> Test Results (if nothing appears, PHP is not working):</H1>
<?php
if (isset($_SERVER["PATH_INFO"]) and $_SERVER["PATH_INFO"]=="/this/is/a/test") {
   echo "EXTENDED PATH TEST PASSED! Note this does not mean your CGI works perfectly according to the CGI/1.1 spec, but it at least passed the test.";
}
else {
   echo "EXTENDED PATH TEST FAILED! Your CGI is not working correctly.";
}

?> 
 </body>
</html>