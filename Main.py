#then create location
#imports
import socket
import threading
import os
#Variables
#IP=socket.gethostbyname("localhost") #IP Address
IP=socket.gethostbyname(socket.gethostname()) #IP All Usage
print(IP)
Port=80 #Standard HTTP Port Number
BIND_VAR=(IP,Port) #Bindvariables for Socket Usae Later
size=1024 #data receive size
format="utf-8"

#"""Main Methods"""
#Get Method
def process_GET(conn,data):
    #file path    
    file_directory=b'AllFiles'   
    response=b''        
    #Studies Stripped data for location folder and then send the data back   
    location_data=data[1]
    #check for file type given or not
    html_check=location_data.find(b'html')
    htm_check=location_data.find(b'htm')
    #address given check
    location_depth=location_data.find(file_directory)
    if location_depth != -1:
        temp_data=location_data[location_depth:]
        #try to find data in location
        try:
            if html_check == -1 and htm_check ==-1:
                try:
                    temp_file=open(temp_data+ b'.html')
                    temp_data=temp_data + b'.html'
                except:
                    temp_data=temp_data + b'.htm'                    
            file=open(temp_data)
            filedata=file.read()
            response += bytes(filedata.encode(format))
            if data[2] == b'HTTP/0.9' :  
                response += b'\r\n\r\n'            
                conn.send(response)
            else:                
                #need to add headers
                response += b'\r\n\r\n'            
                conn.send(response)
        #if file not found send 404 response
        except:
            final_location=file_directory + b'/404.html'
            file= open(final_location)
            filedata = file.read()        
            response += bytes(filedata.encode(format))
            if data[2] == b'HTTP/0.9' :  
                response += b'\r\n\r\n'            
                conn.send(response)
            else:                
                #need to add headers
                response += b'\r\n\r\n'            
                conn.send(response)    
    #if only file called      
    else:           
        final_location=file_directory + location_data 
        try:   
            if html_check == -1 and htm_check ==-1:
                try:
                    temp_file=open(final_location+ b'.html')
                    final_location=final_location + b'.html'
                except:
                    final_location=final_location + b'.htm'               
            file= open(final_location)
            filedata = file.read()        
            response += bytes(filedata.encode(format))
            if data[2] == b'HTTP/0.9' :  
                response += b'\r\n\r\n'            
                conn.send(response)
            else:                
                #need to add headers
                response += b'\r\n\r\n'            
                conn.send(response)
        except:
            final_location=file_directory + b'/404.html'
            file= open(final_location)
            filedata = file.read()        
            response += bytes(filedata.encode(format))
            if data[2] == b'HTTP/0.9' :  
                response += b'\r\n\r\n'            
                conn.send(response)
            else:                
                #need to add headers
                response += b'\r\n\r\n'            
                conn.send(response)               
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
                if  line_end != -1:
                        return data[:line_end]
            except:
                return -1
    
#Method to Process CLient
def client_process(conn,clientid):
    data=recv_data(conn)    
    if data == -1:
        conn.close()
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
    conn.close()
    
       
    
#Method to start connection
def main():    
    #creating Seperate Threads       
    web_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    web_server.bind(BIND_VAR)
    web_server.listen(True)
    #infinite loop for accepting clients
    while True: 
        conn,clientid=web_server.accept()
        new_client1=threading.Thread(target=client_process,args=(conn,clientid))
        new_client1.start()
        print(f"{repr(clientid)} has established a new connection.")

main()