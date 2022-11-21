<html>
<!-- WHAT FOLLOWS IS HTML AND PHP CODE. IF THE CODE IS BEING DISPLAYED IN YOUR BROWSER, YOU DID NOT GET PHP WORKING YET... -->
 <head>
  <title>PHP Test for correctly informing PHP of the user's web browser (or HTTP client)</title>
 </head>
 <body>
<H1> Test Results (if nothing appears, PHP is not working):</H1>
<?php
if (isset($_SERVER["HTTP_USER_AGENT"])) {
   echo "BROWSER IDENTIFICATION TEST PASSED! ";
   echo "PHP has identified your browser (or HTTP client) as ";
   echo $_SERVER["HTTP_USER_AGENT"];
   echo ". Note this does not mean your CGI works perfectly according to the CGI/1.1 spec, but it at least passed the test.";
}
else {
   echo "BROWSER IDENTIFICATION TEST FAILED! To get this test to work correctly, you need to be familiar with Section 4.1.18 of RFC 3875 and Section 10.15 of RFC 1945.";
}

?> 
 </body>
</html>