import socket
import json
import os
from datetime import datetime

def receive_messages(server_ip, server_port):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  #AF_INET is the standard for IPv4 and SOCK_STREAM defines the connection to be over TCP
        # Connect to server
        sock.connect((server_ip, server_port))
    
        
        while True:
        #for i in range(10):
            #print("receive new message")
            
            # Initialize variables for message assembly
            buffer = b''  # Buffer to accumulate received data
            receiving_message = False  # Flag to indicate if currently receiving a message
            current_message = b''  # Variable to store the currently assembling message
            
        
            data = sock.recv(6000)  # Receive data (adjust buffer size as needed
            if not data:
                break
            
            buffer += data
            #print(buffer)
            
            while buffer:
                if not receiving_message:
                    # Look for the start of a new message
                    #start_index = buffer.find(b'{"message type"')
                    start_index = buffer.find(b'{')
                    
                    if start_index != -1:
                        #print("dsfgsdfgsdfgdf")
                        # Discard any previous incomplete message
                        buffer = buffer[start_index:]
                        receiving_message = True
                        current_message = b''
                    else:
                        buffer = b''  # If no start found, clear buffer
                else:
                    #print("receive message")
                    # Continue assembling the current message
                    null_index = buffer.find(b'\x00')-6
                    #null_index = buffer.find(b'}')+1
                    #print(null_index)
                    if null_index != -1:
                        # Found the end of the message
                        message_data = buffer[:null_index]
                        current_message += message_data
                        
                            
                        process_message(current_message)  # Process the assembled message
                        # Reset flags and buffers for next message
                        receiving_message = False
                        current_message = b''
                        buffer = buffer[null_index + 1:]
                        #print("test")
                    else:
                        current_message += buffer
                        buffer = b''
            
    sock.close()                     
    return 1;                    
            
def process_message(data):
    # Process the JSON-encoded message
    try:
        #data = data[:-6]
        message_json = data.decode('utf-8')
        message_obj = json.loads(message_json)
        print("Received message:", message_obj["message type"])
        #print(message_obj)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        print(data)
        #print(data)
    except Exception as e:
        print("Error processing message:", e)

# Example usage
if __name__ == "__main__":
    server_ip = '134.61.142.154'
    server_port = 50000  # Replace with your server's port
    booli=receive_messages(server_ip, server_port)
    if(booli==0):
        print("Data not found")
        
