import socket
import struct

def calculate_checksum_ones_complement(data):
    checksum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + (data[i + 1] if i + 1 < len(data) else 0)
        checksum += word
        checksum = (checksum & 0xFFFF) + (checksum >> 16) 
    return ~checksum & 0xFFFF 

def encapsulate_message(source_port, dest_port, data):
    length = len(data)
    other_header_fields = 0x1234  
    header = struct.pack('!HHHH', source_port, dest_port, length, other_header_fields)
    checksum = calculate_checksum_ones_complement(header + data)
    return header + data + struct.pack('!H', checksum) 

def extract_message(encapsulated_response):
    header = encapsulated_response[:8]  
    source_port, dest_port, length, other_header_fields = struct.unpack('!HHHH', header)
    data = encapsulated_response[8:8+length]
    received_checksum = struct.unpack('!H', encapsulated_response[8+length:8+length+2])[0]


    print("Client Received Encapsulated Acknowledgment from Server:")
    print(f"  Source Port: {source_port}")
    print(f"  Destination Port: {dest_port}")
    print(f"  Length: {length} bytes")
    print(f"  Other Header Fields: {hex(other_header_fields)}")
    print(f"  Application Data: {data.decode()}")
    print(f"  Server Checksum: {received_checksum}")
    print("-" * 50)

    return data.decode(), received_checksum

def run_client():
    server_ip = '172.16.1.21'
    server_port = 12000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('0.0.0.0', 0))
    source_port = client_socket.getsockname()[1] 

    while True:
        message = input("Enter message (or 'q' to quit): ")
        if message.lower() == 'q':
            break
        data = message.encode()
        encapsulated_message = encapsulate_message(source_port, server_port, data)
        client_socket.sendto(encapsulated_message, (server_ip, server_port))
        response, _ = client_socket.recvfrom(1024)
        decoded_acknowledgment, server_checksum = extract_message(response)
        print(f"Received acknowledgment from server with checksum: {server_checksum}: {decoded_acknowledgment}")

    client_socket.close()

if __name__ == "__main__":
    run_client()
