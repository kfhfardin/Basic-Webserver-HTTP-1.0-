#then create location
#imports
import socket
import threading
import os
import datetime
#Variables
#IP=socket.gethostbyname("localhost") #IP Address
IP=socket.gethostbyname(socket.gethostname()) #IP All Usage
# IP if-statement
if socket.gethostname() == 'Khois-MacBook-Pro.local':
    IP="10.30.69.119" #IP for Khoi
Port=80 #Standard HTTP Port Number
unprivileged_port=2021 #Port for unprivileged users
BIND_VAR=(IP,Port) #Bind variables for Socket Use Later
size=1024 #data receive size
format="utf-8"

# Dictionaries for IANA MIME Types from File Extensions
"""
text/
.js: text/javascript
.py: text/x-script.phyton
.txt: text/plain
.css: text/css
.htm: text/html
.html: text/html
"""
txt_std_ext={".js":"text/javascript", ".py":"text/x-script.phyton", ".txt":"text/plain", ".css": "text/css", ".htm":"text/html", ".html":"text/html"}
"""
applicaton/
.pdf: application/pdf
.rtf: application/rtf
.zip: application/zip
.jar: application/java-archive
.doc: application/msword
.docx: application/vnd.openxmlformats-officedocument.wordprocessingml.document
.json: application/geo+json
.xml: application/xhtml+xml
.xhtml: application/xhtml+xml
.php: application/x-httpd-php
"""
app_std_ext={".pdf":"application/pdf", ".rtf":"application/rtf", ".zip":"application/zip", ".jar":"application/java-archive", ".doc":"application/msword", ".docx":"application/vnd.openxmlformats-officedocument.wordprocessingml.document", ".json":"application/geo+json", ".xml":"application/xhtml+xml", ".xhtml":"application/xhtml+xml", ".php":"application/x-httpd-php"}
"""
image/
.gif: image/gif
.png: image/png
.bmp: image/bmp
.ico: image/vnd.microsoft.icon
.jpx: image/jpx
.jp2: image/jp2
.jpg: image/jpeg
.jpeg: image/jpeg
.apng: image/apng
.webp: image/webp
"""
img_std_ext={".gif":"image/gif", ".png":"image/png", ".bmp":"image/bmp", ".ico":"image/vnd.microsoft.icon", ".jpx":"image/jpx", ".jp2":"image/jp2", ".jpg":"image/jpeg", ".jpeg":"image/jpeg", ".apng":"image/apng", ".webp":"image/webp"}
"""
audio/
.mp3: audio/mpeg3
.wav: audio/wav
.mpg: audio/mpeg
"""
audio_std_ext={".mp3":"audio/mpeg3", ".wav":"audio/wav", ".mpg":"audio/mpeg"}
"""
video/
.avi: video/x-msvideo
.mpeg: video/mpeg
"""
video_std_ext={".avi":"video/x-msvideo", ".mpeg":"video/mpeg"}

# Merging all dictionaries for conversions to MIME type
iana_dict = {**txt_std_ext, **app_std_ext, **audio_std_ext, **img_std_ext, **video_std_ext}

#"""MAIN METHODS"""

# Method to get supported MIME types
def mime_type(file_ext):
    try:
        kind = iana_dict[".xlsx"]
    except:
        kind = None
    return kind

# Method to get local time
def local_time():
    dt = datetime.datetime.now().strftime("%a, %d-%b-%Y %H:%M:%S Local-Time")
    return f"{dt}"

# Method to get local time in accordance with HTTP/1.0
def http_time():
    dt = datetime.datetime.now(datetime.timezone.utc)
    utc_time = dt.replace(tzinfo=datetime.timezone.utc)
    http_time = utc_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return f"{http_time}"

# Method to generate a HTTP/1.0 status line
def http_1_0_status(code=500, reason=None, version="1.0"): # Need to update if 1.1 but DONT CHANGE the default
    version = f"HTTP/{version}"
    fields = [version,code,reason]
    status_str = ""
    k=0
    for i in fields:
        if i!=None and k==0:
            status_str += f"{i}"
            k+=1
        elif i!=None:
            status_str += f" {i}"
    return f"{status_str}\r\n"

# HEADER FUNCTIONS
# By default, most parameters are set to None. If None, those parameters will not be outputted onto the HTTP message.
# So, when calling these Header functions, make sure to set those parameters to value in line with RFC1945 HTTP/1.0.
def general_header(pragma=None,time=http_time()):
    header_str = ""
    fields = [time,pragma]
    field_name = ["Time", "Pragma"]
    for i in fields:
        if i!=None:
            header_str += f"{field_name[fields.index(i)]}: {i}\r\n"
    return f"{header_str}"

def response_header(location=None, authentication=None, server= f"EvanFardinKhoi/0.1"):
    header_str = ""
    fields = [location,server,authentication]
    field_name = ["Location", "Server","WWW-Authenticate"]
    for i in fields:
        if i!=None:
            header_str += f"{field_name[fields.index(i)]}: {i}\r\n"
    return f"{header_str}"

def entity_header(allow=None, encoding=None, length=None, type=None, expiry=None, last_edit=None, ext=None):
    header_str = ""
    fields = [allow,encoding,length,type,expiry,last_edit,ext]
    field_name = ["Allow","Content-Encoding","Content-Length","Content-Type","Expires","Last-Modified"]
    for i in fields:
        if i!=None:
            if i!=ext:
                header_str += f"{field_name[fields.index(i)]}: {i}\r\n"
            else:
                header_str += f"{i}\r\n"
    return f"{header_str}"



# GET Method
def process_GET(conn,data_ls,HEAD_request=False):
    # file path    
    file_directory=b'AllFiles'   
    response=b''        
    # Studies Stripped data for location folder and then send the data back   
    location_data=data_ls[1]
    # check for file type given or not
    temp_type_val= ""
    content_type_val= ""          
    # add if and else statements
    # address given check
    #HTTP 0.9 check
    try:
        http_0_9 = b'HTTP' not in data_ls[2]
    except:
        http_0_9 = True
    
    location_depth=location_data.find(file_directory)
    if location_depth != -1:
        # temp_data=location_data[location_depth:]
        # try to find data in location
        try: 
            final_location=location_data[location_depth:]  
            print(final_location)                      
            with open(final_location,'br') as file:
                print(f"\n\r---> Server Identified File: {repr(file)}")
                filedata = file.read()      
            
            if http_0_9:  
                resp_status_headers = str(response)
                if not HEAD_request:
                    response += bytes(filedata.encode(format))
                response += b'\r\n\r\n'
                conn.send(response)
            else:                
                # need to add headers
                status = http_1_0_status(200)
                response += bytes(f"{status}".encode(format))
                # This is where we need to find our content types
                headers = f"{general_header()}{response_header()}{entity_header()}\r\n"  
                response += bytes(headers.encode(format))
                resp_status_headers = response
                if not HEAD_request:
                    response += filedata
                response += b'\r\n\r\n'
                conn.send(response)
        # if file not found send 404 response
        except:
            final_location=file_directory + b'/404.html'
            with open(final_location,'br') as file:
                print(f"\n\r---> Server Identified File: {repr(file)}")
                filedata = file.read()        
            if http_0_9:  
                resp_status_headers = str(response)
                if not HEAD_request:
                    response += filedata
                response += b'\r\n\r\n'           
                conn.send(response)
            else:                
                # need to add headers
                status = http_1_0_status(404)
                response += bytes(f"{status}".encode(format))
                headers = f"{general_header()}{response_header()}{entity_header()}\r\n"
                response += bytes(headers.encode(format))
                resp_status_headers = response
                if not HEAD_request:
                    response += filedata
                response += b'\r\n\r\n'            
                conn.send(response)    
    # if only file called      
    else:           
        final_location=file_directory + location_data 
        print(f"\n\r-> Client Requested File-Location: {repr(final_location)}")
        try:   
            with open(final_location,'br') as file:
                print(f"\n\r---> Server Identified File: {repr(file)}")
                filedata = file.read()
            print(f"\n\r------> File-Content extracted successfully!")

            if http_0_9:  
                resp_status_headers = str(response)
                if not HEAD_request:
                    response += filedata
                response += b'\r\n\r\n'       
                conn.send(response)
            else:                
                status = http_1_0_status(200)
                response += bytes(f"{status}".encode(format))
                headers = f"{general_header()}{response_header()}{entity_header()}\r\n"
                response += bytes(headers.encode(format))
                resp_status_headers = response
                if not HEAD_request:
                    response += (filedata)
                response += b'\r\n\r\n'            
                conn.send(response)
        except:
            print(f"\n\r------> File NOT located!")
            final_location=file_directory + b'/404.html'
            with open(final_location,'br') as file:
                print(f"\n\r---> Server Identified File: {repr(file)}")
                filedata = file.read()      
            
            if http_0_9:  
                resp_status_headers = str(response)
                if not HEAD_request:
                    response += filedata
                response += b'\r\n\r\n'
                conn.send(response)
            else:               
                status = http_1_0_status(404)
                response += bytes(f"{status}".encode(format))
                headers = f"{general_header()}{response_header()}{entity_header()}\r\n"
                response += bytes(headers.encode(format))
                resp_status_headers = response
                if not HEAD_request:
                    response += filedata
                response += b'\r\n\r\n'            
                conn.send(response)               
    if not HEAD_request:
        print(f"\n\r-> Server responded on ({local_time()})::\n\r{resp_status_headers}{file}\\r\\n\\r\\n")
    elif HEAD_request:
        print(f"\n\r-> Server responded on ({local_time()})::\n\r{response}")
    return

# HEAD method
def process_HEAD(conn,data):
    process_GET(conn,data,HEAD_request=True)

# POST Method
def process_POST(conn,data):
    x=0

# Method to Receive Data
def recv_data(conn):
        data=b''
        while True:
            try:
                temp_data=conn.recv(size)
                if temp_data == b'':
                    print(f"\n\rServer has killed a connection on {http_time()}")
                    conn.close()
                data+=temp_data
                line_end= data.find(b'\r\n\r\n')
                print(f"\n\r-> Server intercepted on ({local_time()}):\n\r{repr(data)}")
                if  line_end != -1:
                        return data[:line_end]
            except:
                return -1
    
# Method to Process CLient
def client_process(conn,clientid):
    data=recv_data(conn)
    print(f"\n\r-> Package processed on ({local_time()}):\n\r{repr(data)}")
    if data == -1:
        conn.close()
        print(f"\n\r{repr(clientid)} has disconnected on {http_time()}")
        return
    # request method checks
    # splitting data into parts
    split_data=data.split()
    print(split_data)
    # GET check
    if split_data[0]== b'GET':
        process_GET(conn,split_data)        
    # HEAD check    
    if split_data[0]== b'HEAD':
        process_HEAD(conn,split_data)    
        
    # POST check    
    if split_data[0]== b'POST':
        process_POST(conn,split_data)
    # closing connection
    print(f"\n\r-> Closed connection -x-> {repr(clientid)} on {local_time()}")
    conn.close()
    
       
    
# Method to start connection
def main():    
    # creating Seperate Threads       
    web_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        web_server.bind(BIND_VAR)
    except:
        Port=unprivileged_port
        BIND_VAR=(IP,Port)
        web_server.bind(BIND_VAR)
    web_server.listen(True)
    print(f"\n\r\n\rServer is now running.\n\rClients can establish new connections to http://{IP}:{Port}/\n\r")
    if IP=='127.0.0.1':
        print(f"The current host IP is a loopback address, so only this machine can connect to the current server.\n\rPlease manually check for your IPv4 address then enter it to if-statement for IP address on line 10.\n\r")
    # infinite loop for accepting clients
    while True: 
        conn,clientid=web_server.accept()
        new_client1=threading.Thread(target=client_process,args=(conn,clientid))
        new_client1.start()
        conn_time = http_time()
        print(f"\n\rNew connection established ---> {repr(clientid)} on ({conn_time})")

main()

#--------------------------------------------------------
# For WOW factor I want to download multiple files for one connection
# HTTP 1.0 closes the connection in between each file, but 1.1 does not close the connection each time
# To do this I need to understand the problem, try to figure out how to code and talk with Fardin
#--------------------------------------------------------
