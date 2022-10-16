# CSC-271-Project-02-<br>
## This is the Update Page.<br>
#### Everytime a change is made a short update  of the change is written here with name.<br>
#### Also comment the date,time and name of any updaates made in the comment section<br>

### Update on 8/10/2022 (10 PM)(Fardin)<br>
This is the first commit to the page.<br>
The commit contains:<br> 
1. 2 tests provided by the Professor
2. main python file
3. readme document
4. Ability to access HelloWorld.html
5. check for html and htm
6. Ability to access files with different paths provided

Things to be done:<br>
1. Figure out how to access subdirectory
2. Figure out output and input  for Post and Head
3. Figure out CGI extension

### Update on 9/10/2022 (4 PM) (Khoi)<br>
Added header methods.
Added server-side status outputs.

### Update on 10/10/2022 (5 PM) (Khoi)<br>
Added with open statement to open, read, and close files
--> .img files can now be opened properly, due to the 'br' option
--> Changed how the print(response) function behaves under GET request. Now it only prints out a shortened version of the response to GET.

### Update on 11/10/2022 (1 PM) (Evan and Khoi)<br>
fixed the inf b'' sending error

### Update on 12/10/2022 (0 AM) (Khoi)<br>
Major updates to: IP & Port check, GET & HEAD methods, MIME type assignment method
1. Code now checks for loopback IP address. If detected, it'll print out a note on server side.
2. Code now checks for permission to run on default port 80. If error, server will now be automatically be redirected to the unprivileged_port instead.
3. Added a method that takes in file extensions and return their corresponding MIME types in accordance with IANA.
4. Modify GET method to not include Entity-Body when the HEAD method calls it instead.
5. Added HEAD method, which "is identical to GET except that the server must not return any Entity-Body in the response" (RFC 1945).

# Update on 15-16/10/2022 (Khoi) <br>
If the request-path contains a file-name without an extension, the server now makes a guess and attach an extension according to what is available on the current folder's content