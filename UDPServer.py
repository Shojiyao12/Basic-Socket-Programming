import socket
import struct

def calculate_checksum_ones_complement(data):
    checksum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + (data[i + 1] if i + 1 < len(data) else 0)
        checksum += word
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    
    return ~checksum & 0xFFFF  

def encapsulate_message(source_port, dest_port, other_header_fields, data):
    """Encapsulate the message with source port, destination port, and other headers."""
    length = len(data)  # Length of the data
    header = struct.pack('!HHHH', source_port, dest_port, length, other_header_fields)
    checksum = calculate_checksum_ones_complement(header + data)
    encapsulated_message = header + data + struct.pack('!H', checksum)
    return encapsulated_message

def verify_checksum_ones_complement(header, data, received_checksum):
    """Verify the checksum by recalculating it from the received header and data."""
    computed_checksum = calculate_checksum_ones_complement(header + data)
    return computed_checksum == received_checksum

def handle_client(connection, server_port):
    """Handle client messages, encapsulate, and confirm checksum."""
    while True:
        try:
            encapsulated_message, client_address = connection.recvfrom(1024)

            if not encapsulated_message:
                break

            header = encapsulated_message[:8] 
            source_port, dest_port, length, other_header_fields = struct.unpack('!HHHH', header)

            data = encapsulated_message[8:8+length]
            received_checksum = struct.unpack('!H', encapsulated_message[8+length:8+length+2])[0] 

            if verify_checksum_ones_complement(header, data, received_checksum):
                print("Server Received Encapsulated Message from Client:")
                print(f"  Source Port: {source_port}")
                print(f"  Destination Port: {dest_port}")
                print(f"  Length: {length} bytes")
                print(f"  Other Header Fields: {hex(other_header_fields)}")
                print(f"  Application Data: {data.decode()}")
                print(f"  Client Checksum: {received_checksum}")
                print("-" * 50)

                ack_message = b"Acknowledged"
                encapsulated_ack = encapsulate_message(server_port, source_port, 0x1234, ack_message)
                connection.sendto(encapsulated_ack, client_address)
            else:
                print(f"Invalid checksum from {client_address}. Message corrupted.")
                connection.sendto(b'Checksum invalid. Message corrupted.', client_address)

        except ConnectionError as e:
            print(f"Connection error: {e}")
            break

def start_server():
    server_port = 12000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', server_port))
    print(f"Server listening on port {server_port}")
    while True:
        try:
            handle_client(server_socket, server_port)
        except KeyboardInterrupt:
            print("Server shutting down...")
            break
if __name__ == "__main__":
    start_server()
