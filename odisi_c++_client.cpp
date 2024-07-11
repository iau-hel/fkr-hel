#include <iostream>
#include <cstring>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <conio.h>
#include <fstream>
#include "json.hpp"
#include <string>
#include <array>
#include <algorithm>

#pragma comment(lib, "Ws2_32.lib")

bool formatJSON(const std::string& data) {
    std::string trimmedData = data;
    trimmedData.erase(0, trimmedData.find_first_not_of(" \t\n\r\f\v"));
    trimmedData.erase(trimmedData.find_last_not_of(" \t\n\\f\v") + 1);

        if (trimmedData.empty() || (trimmedData[0] != '{' && trimmedData[0] !='[')){
            return false;
        }
        
    try {
        nlohmann::json jsonData = nlohmann::json::parse(trimmedData);
        return true;
    }
    catch (const nlohmann::json::exception& e) {
        return false;
        }

}


int main() {
    const char* server_ip = "134.61.142.154";
    const int server_port = 50000;
    WSADATA wsaData;
    int wsaInit = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (wsaInit != 0) {
        std::cerr << "WSAStartup failed: " << wsaInit << std::endl;
        return 1;
    }
    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == INVALID_SOCKET) {
        std::cerr << "Error creating socket: " << WSAGetLastError() << std::endl;
        WSACleanup();
        return 1;
    }

    sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(server_port);
    if (inet_pton(AF_INET, server_ip, &server_addr.sin_addr) <= 0) {
        std::cerr << "Invalid address/Address not supported" << std::endl;
        closesocket(sock);
        WSACleanup();
        return 1;
    }
    if (connect(sock, (sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        std::cerr << "Connection failed: " << WSAGetLastError() << std::endl;
        closesocket(sock);
        WSACleanup();
        return 1;
    }
    std::cout << "Connected to server successfully" << std::endl;


    char press = '0';
    std::array<char,20000> buffer;
   // char buffer[20000];
    std::ofstream outfile;
    std::ofstream outfile2;
    outfile.open("H:\data.txt");
    outfile2.open("H:\data2.txt");
    int bytesReceived = recv(sock, buffer, sizeof(buffer) - 1, 0);
    std::string receivedJSON;
    if (bytesReceived > 0) {
        buffer[bytesReceived] = '\0';
        std::cout << "Type of data received: char" << std::endl;
        std::cout << "Size of data received: " << bytesReceived << " bytes" << std::endl;
        std::cout << "Data received from server: " << buffer << std::endl;
        int it=0;
           for (const auto& elem : buffer) {
        it++;
        if (elem == '}') {
            break;
        }
    }

    // Create a character array with size it + 1 for the null terminator
    char receivedJSON[it + 1];
    
    // Copy elements from buffer to receivedJSON
    for (int i = 0; i < it; i++) {
        receivedJSON[i] = buffer[i];
    }

    // Null-terminate the string
    receivedJSON[it] = '\0';

   

  

        }
        if (formatJSON(receivedJSON)) {

            try {
                nlohmann::json jsonData=nlohmann::json::parse(receivedJSON);
                //recv(sock,reinterpret_cast<char*>(&jsonData),sizeof(jsonData),0);
                if (outfile2.is_open()) {
                    std::cout << "fsdfjsdfjsdfjsdf" << std::endl;

                    if (jsonData["message type"] == "metadata") {
                        std::cout << "File is opened" << std::endl;
                        outfile2 << "Test name: " << jsonData["test name"] << std::endl;
                        std::cout << "kjfkgsdksdfksdfhksdaf" << std::endl;
                        outfile2 << "Notes: " << jsonData["notes"] << std::endl;
                        outfile2 << "Product: " << jsonData["product"] << std::endl;
                        outfile2 << "Software version: " << jsonData["software version"] << std::endl;
                        outfile2 << "Hardware Version: " << jsonData["hardware version"] << std::endl;
                        outfile2 << "Firmware version: 1.6.14 (03/24/2021)" << std::endl;
                        outfile2 << "FPGA Version: v7.3.8-15016 (03/02/21)" << std::endl;
                        outfile2 << "Measurement Rate Per Channel: " << jsonData["measurement rate"] << std::endl;
                        outfile2 << "Spatial Average Window size (gages): " << sizeof(jsonData["gages"]) << std::endl;
                        outfile2 << "Temporal Average Window size (gages): " << sizeof(jsonData["gages"]) << std::endl;
                        outfile2 << "channel: " << jsonData["sensors"][0]["channel"] << std::endl;
                        outfile2 << "Sensor Name: " << jsonData["sensors"][0]["sensor name"] << std::endl;
                        outfile2 << "Sensor Serial Number: " << jsonData["sensors"][0]["sensor serial number"] << std::endl;
                        outfile2 << "Sensor Part Number: " << jsonData["sensors"][0]["sensor part number"] << std::endl;
                        outfile2 << "Sensor Type: " << jsonData["sensors"][0]["sensor type"] << std::endl;
                        outfile2 << "Units: " << jsonData["sensors"][0]["units"] << std::endl;
                        outfile2 << "x-axis units: m" << std::endl;
                        outfile2 << "Length (m): " << jsonData["sensors"][0]["lenght"] << std::endl;


                    }
                    if (jsonData["message type"] == "measurement") {
                        outfile2 << "Date: " << jsonData["year"] << "-" << jsonData["month"] << "-" << jsonData["day"] << " " << jsonData["hours"] << ":" << jsonData["minutes"] << ":" << jsonData["seconds"] << jsonData["milliseconds"] << std::endl;
                        outfile2 << "Timezone: " << jsonData["time zone"] << std::endl;
                        outfile2 << "File Type: ODiSI 6xxx Data File " << std::endl;
                        outfile2 << "File version: 8" << std::endl;
                        outfile2 << "System Serial Number: " << jsonData["system serial number"] << std::endl;
                        outfile2 << "Gage Pitch: " << jsonData["gage pitch"] << std::endl;
                        outfile2 << "Key name: " << jsonData["sensors"][0]["sensor key name"] << std::endl;
                    }

                    outfile2 << "Standoff cable lenght: 50" << std::endl;
                    outfile2 << "Temperature offset: 0" << std::endl;
                    outfile2 << "Performance Mode: Full Optimization" << std::endl;
                    outfile2 << "Patch Cord length (m): 0" << std::endl;

                    if (jsonData["message type"] == "tare") {
                        outfile2 << "Tare name: " << jsonData["tare name"] << std::endl;
                        outfile2 << "Tare : " << jsonData["data"] << std::endl;
                    }


                    outfile2.flush();
                    std::cout << "Writing JSON into file" << std::endl;
                }
               else {
                  std::cout << "Error 404" << std::endl;
                }
            }
            catch (nlohmann::json::parse_error& e) {
                std::cerr << "Failed to parse JSON data: " << e.what() << std::endl;
            }
       }
       else {
         std::cerr << "Received Data not in JSON Format " << std::endl;
        }
    }
    else if (bytesReceived == 0) {
        std::cout << "Connection closed by server." << std::endl;
       
    }
    else {
        std::cerr << "recv failed: " << WSAGetLastError() << std::endl;
       
    }

    while (true) {

        bytesReceived = recv(sock, buffer, sizeof(buffer) - 1, 0);
        receivedJSON = buffer;
        if (bytesReceived > 0) {
            buffer[bytesReceived] = '\0';
            std::cout << "Type of data received: char" << std::endl;
            std::cout << "Size of data received: " << bytesReceived << " bytes" << std::endl;
            std::cout << "Data received from server: " << receivedJSON << std::endl;

            
            if (formatJSON(receivedJSON)) {
                try {
                    nlohmann::json jsonData = nlohmann::json::parse(receivedJSON);
                    if (outfile2.is_open()) {
                        std::cout << "File is opened" << std::endl;
                        if (jsonData["measurement type"] == "measurement") {
                            outfile2 << jsonData["year"] << "-" << jsonData["month"] << "-" << jsonData["day"] << " " << jsonData["hours"] << ":" << jsonData["minutes"] << ":" << jsonData["seconds"] << jsonData["milliseconds"];
                            outfile2 << jsonData["measurement type"];
                            outfile2 << jsonData["sensor type"];
                            outfile2 << jsonData["data"] << std::endl;
                        }
                        outfile2.flush();
                        std::cout << "Writing JSON into file" << std::endl;
                    }
                    else {
                        std::cout << "Error 404" << std::endl;
                    }
                }
                catch (nlohmann::json::parse_error& e) {
                    std::cerr << "Failed to parse JSON data: " << e.what() << std::endl;
                }
            }
            else {
                std::cerr << "Received Data not in JSON Format" << std::endl;
            }
        }
        else if (bytesReceived == 0) {
            std::cout << "Connection closed by server." << std::endl;
            break;
        }
        else {
            std::cerr << "recv failed: " << WSAGetLastError() << std::endl;
            break;
        }
        if (_kbhit()) {
            press = _getch();
            if (press == 'e' || press == 'E') {
                std::cout << "Server is disconnected" << std::endl;
                break;
            }
        }
    }
    outfile.close();
    std::cout << "File closed" << std::endl;
    closesocket(sock);
    WSACleanup();

    return 0;
}
   