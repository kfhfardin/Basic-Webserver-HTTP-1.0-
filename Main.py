#then create location
#imports
import socket
import threading
import os
import datetime
#Variables
#IP=socket.gethostbyname("localhost") #IP Address
IP=socket.gethostbyname(socket.gethostname()) #IP All Usage
#IP="10.30.69.119" #IP for Khoi
Port=80 #Standard HTTP Port Number
#Port=2022 #Port for unprivileged users
BIND_VAR=(IP,Port) #Bindvariables for Socket Usae Later
size=1024 #data receive size
format="utf-8"
file_ext_list=[]
std_ext_dict=[]
iana_dict={}

#"""Main Methods"""
def local_time():
    dt = datetime.datetime.now().strftime("%a, %d-%b-%Y %H:%M:%S Local-Time")
    return f"{dt}"

def http_time():
    dt = datetime.datetime.now(datetime.timezone.utc)
    utc_time = dt.replace(tzinfo=datetime.timezone.utc)
    http_time = utc_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return f"{http_time}"

def http_1_0_status(code=500, reason=None, version="1.0"):
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



#Get Method
def process_GET(conn,data):
    #file path    
    file_directory=b'AllFiles'   
    response=b''        
    #Studies Stripped data for location folder and then send the data back   
    location_data=data[1]
    #check for file type given or not
    temp_type_val= ""
    content_type_val= ""
    switch=False
    i=0
    while switch is False:
        index_val=location_data.find(file_ext_list[i])
        if index_val != -1:
            switch=True
            general_type=iana_dict[file_ext_list[i]]
            content_type_val= general_type +'/'+file_ext_list[i]
            temp_type_val=file_ext_list[i]
        i+=1
      
    
    # if  content_type_val == "" :         
    #     try:
    #         temp_file=open(temp_data+ b'.html')
    #         temp_data=temp_data + b'.html'
    #     except:
    #         temp_data=temp_data + b'.htm'            

    
    
    #add if and else statements
    #address given check
    location_depth=location_data.find(file_directory)
    if location_depth != -1:
        temp_data=location_data[location_depth:]
        #try to find data in location
        try:
            # if html_check == -1 and htm_check ==-1:
            #     try:
            #         temp_file=open(temp_data+ b'.html')
            #         temp_data=temp_data + b'.html'
            #     except:
            #         temp_data=temp_data + b'.htm'                    
            file=open(temp_data)
            filedata=file.read()
            
            if data[2] == b'HTTP/0.9' :  
                response += bytes(filedata.encode(format))
                response += b'\r\n\r\n'            
                conn.send(response)
            else:                
                #need to add headers
                status = http_1_0_status(200)
                response += bytes(f"{status}".encode(format))
                headers = f"{general_header()}{response_header()}{entity_header()}\r\n"  
                response += bytes(headers.encode(format))
                response += bytes(filedata.encode(format))
                response += b'\r\n\r\n'
                conn.send(response)
        #if file not found send 404 response
        except:
            final_location=file_directory + b'/404.html'
            file= open(final_location)
            filedata = file.read()        
            
            if data[2] == b'HTTP/0.9' :  
                response += bytes(filedata.encode(format))
                response += b'\r\n\r\n'            
                conn.send(response)
            else:                
                #need to add headers
                status = http_1_0_status(404)
                response += bytes(f"{status}".encode(format))
                headers = f"{general_header()}{response_header()}{entity_header()}\r\n"
                response += bytes(headers.encode(format))
                response += bytes(filedata.encode(format))
                response += b'\r\n\r\n'            
                conn.send(response)    
    #if only file called      
    else:           
        final_location=file_directory + location_data 
        print(f"\n\r-> Client Requested File-Location: {repr(final_location)}")
        try:   
            with open(final_location,'br') as file:
                print(f"\n\r---> Server Identified File: {repr(file)}")
                filedata = file.read()
            print(f"\n\r------> File-Content extracted successfully!")

            if data[2] == b'HTTP/0.9' :  
                response += bytes(filedata.encode(format))
                response += b'\r\n\r\n'            
                conn.send(response)
            else:                
                status = http_1_0_status(200)
                response += bytes(f"{status}".encode(format))
                headers = f"{general_header()}{response_header()}{entity_header()}\r\n"
                response += bytes(headers.encode(format))
                response += (filedata)
                response += b'\r\n\r\n'            
                conn.send(response)
        except:
            final_location=file_directory + b'/404.html'
            file= open(final_location)
            filedata = file.read()        
            
            if data[2] == b'HTTP/0.9' :  
                response += bytes(filedata.encode(format))
                response += b'\r\n\r\n'            
                conn.send(response)
            else:               
                status = http_1_0_status(404)
                response += bytes(f"{status}".encode(format))
                headers = f"{general_header()}{response_header()}{entity_header()}\r\n"
                response += bytes(headers.encode(format))
                response += bytes(filedata.encode(format))
                response += b'\r\n\r\n'            
                conn.send(response)               
    print(f"\n\r-> Server responded on ({local_time()})::\n\r{headers}{file}\r\n\r\n")
    return
       
#Head method     
def process_HEAD(conn,data):
    x=0
#Post Method
def process_POST(conn,data):
    x=0

#Method to Receive Data
def recv_data(conn):
        data=b''
        while True:
            try:
                temp_data=conn.recv(size)
                data+=temp_data
                line_end= data.find(b'\r\n\r\n')
                print(f"\n\r-> Server intercepted on ({local_time()}):\n\r{repr(data)}")
                if  line_end != -1:
                        return data[:line_end]
            except:
                return -1
    
#Method to Process CLient
def client_process(conn,clientid):
    data=recv_data(conn)
    print(f"\n\r-> Package processed on ({local_time()}):\n\r{repr(data)}")
    if data == -1:
        conn.close()
        print(f"\n\r{repr(clientid)} has disconnected on {http_time()}")
        return
    #Request method checks
    #splitting data into parts
    split_data=data.split()
    #GET check
    if split_data[0]== b'GET':
        process_GET(conn,split_data)        
    #head_check    
    if split_data[0]== b'HEAD':
        process_HEAD(conn,split_data)    
        
    #post_check    
    if split_data[0]== b'POST':
        process_POST(conn,split_data)
    #closing connection
    print(f"\n\r-> Connection with {repr(clientid)} is closed on {local_time()}")
    conn.close()
    
       
    
#Method to start connection
def main():    
    #creating Seperate Threads       
    web_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    web_server.bind(BIND_VAR)
    web_server.listen(True)
    print(f"\n\r\n\rServer is now running.\n\rClients must establish link to {IP}:{Port}\n\r")
    #infinite loop for accepting clients
    while True: 
        conn,clientid=web_server.accept()
        new_client1=threading.Thread(target=client_process,args=(conn,clientid))
        new_client1.start()
        conn_time = http_time()
        print(f"\n\r({conn_time}) -> {repr(clientid)} has established a new connection.")

main()