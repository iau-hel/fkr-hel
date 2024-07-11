import socket
import json
import os
from datetime import datetime


def receive_messages(server_ip, server_port):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  #AF_INET is the standard for IPv4 and SOCK_STREAM defines the connection to be over TCP
        # Connect to server
        sock.connect((server_ip, server_port))
        outfile_path="H:\data_temp.txt"
        for i in range(10):
            buffer = b''  # Buffer to accumulate received data
            receiving_message = False  # Flag to indicate if currently receiving a message
            current_message = b''  # Variable to store the currently assembling message
            
           
            data = sock.recv(8000)  # Receive data (adjust buffer size as needed
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
                        pre_process_message(current_message,outfile_path,i)  # Process the assembled message
                        # Reset flags and buffers for next message
                        receiving_message = False
                        current_message = b''
                        buffer = buffer[null_index + 1:]
                        #print("test")
                    else:
                        current_message += buffer
                        buffer = b''
        while True:
        #for i in range(10):
            #print("receive new message")
            
            # Initialize variables for message assembly
            buffer = b''  # Buffer to accumulate received data
            receiving_message = False  # Flag to indicate if currently receiving a message
            current_message = b''  # Variable to store the currently assembling message
            
        
            data = sock.recv(8000)  # Receive data (adjust buffer size as needed
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
                        process_message(current_message,outfile_path)  # Process the assembled message
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
def pre_process_message(data,outfile_path,i):
    try:
    #data = data[:-6]
        message_json = data.decode('utf-8')
        message_obj = json.loads(message_json)
        
        if message_obj.get("message type")=="metadata" and i==1:
            
            test_name = message_obj.get("test name", "N/A")
            notes=message_obj.get("notes","N/A")
            product=message_obj.get("product","N/A")
            starting_time=datetime.now()
            formatted_date=starting_time.strftime("%Y-%m-%d")
            formatted_time=starting_time.strftime("%H:%M:%S")
            file_type=message_obj.get("file type","N/A")
            software_version=message_obj.get("software version","N/A")
            hardware_version=message_obj.get("hardware version","N/A")
            firmware_version=message_obj.get("frmware version","N/A")
            measurement_rate=message_obj.get("measurement rate","N/A")
            gage_pitch=message_obj["sensors"][0].get("gage pitch (mm)","N/A")
            channel=message_obj["sensors"][0].get("channel","N/A")
            sensor_name=message_obj["sensors"][0].get("sensor name","N/A")
            sensor_type=message_obj["sensors"][0].get("sensor type","N/A")
            sensor_length=message_obj["sensors"][0].get("length (m)","N/A")
            sensor_units=message_obj["sensors"][0].get("units","N/A")
            
            
            # Open files for writing
            with open(outfile_path, 'a+') as outfile:
                outfile.write(f"Test name: {test_name}\n")
                outfile.write(f"Notes: {notes}\n")
                outfile.write(f"Product: {product}\n")
                outfile.write(f"Date: {formatted_date} {formatted_time}\n")
                outfile.write(f"File type: {file_type}\n")
                outfile.write(f"Software version: {software_version}\n")
                outfile.write(f"Hardware version: {hardware_version}\n")
                outfile.write(f"firmware version: {firmware_version}\n")
                outfile.write(f"Measurement Rate: {measurement_rate} Hz\n")
                outfile.write(f"Gage pitch: {gage_pitch} mm\n")
                outfile.write(f"Channel: {channel}\n")
                outfile.write(f"Sensor Name: {sensor_name}\n")
                outfile.write(f"Sensor Type: {sensor_type}\n")
                outfile.write(f"Sensor length: {sensor_length} m\n")
                outfile.write(f"Sensor units: {sensor_units}\n")
                outfile.close()
            # Do something with the message object
        if message_obj["message type"]=="tare":
                channel=message_obj.get("channel","N/A")
                data_t=message_obj.get("data","N/A")
                with open(outfile_path, 'a+') as outfile:
                     outfile.write(f"Tare: channel {channel}\t{data_t}\n\n")
                     outfile.close()
        print("Receiving Data: ",message_obj["message type"])
        #print(message_obj)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
            #print(data)
    except Exception as e:
        print("Error processing message:", e)
            
def process_message(data,outfile_path):
    # Process the JSON-encoded message
    try:
        #data = data[:-6]
        message_json = data.decode('utf-8')
        message_obj = json.loads(message_json)
        
        if message_obj.get("message type")=="measurement":
            timezone=message_obj.get("timezone","N/A")
            year = message_obj.get("year", "N/A")
            month=message_obj.get("month","N/A")
            day=message_obj.get("day","N/A")
            hours=message_obj.get("hours","N/A")
            minutes=message_obj.get("minutes","N/A")
            seconds= message_obj.get("seconds","N/A")
            milliseconds= message_obj.get("milliseconds","N/A")
            type_m=message_obj.get("message type","N/A")
            type_d=message_obj.get("measurement type","N/A")
            data_m=message_obj.get("data")
            
            # Open files for writing
            with open(outfile_path, 'a+') as outfile:
                outfile.write(f"timezone: {timezone} {year}-{month}-{day} {hours}:{minutes}:{seconds}.{milliseconds}\t{type_m}\t{type_d}\t{data_m}\n\n")
                outfile.close()
            # Do something with the message object
        print("Received message:", message_obj["message type"])
        #print(message_obj)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
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
        
