# Basic-Socket-Programming

# UDP Client-Server Communication

This project implements a UDP-based client-server communication system in Python. The communication follows a structured approach where the client sends encapsulated messages with a checksum, and the server verifies the integrity before acknowledging the received data.

## Quickstart Guide

### Running the Server
1. Copy all the contents from this repository.
2. Open a terminal and navigate to the folder containing the files.
3. Run the **UDPServer.py** file using:
   ```bash
   python UDPServer.py
   ```
4. The server will start listening on `port 12000`.

### Running the Client
1. Open another terminal and navigate to the same folder.
2. Run the **UDPClient.py** file using:
   ```bash
   python UDPClient.py
   ```
3. Enter a message in the client terminal. The client will:
   - Encapsulate the message with a header and checksum.
   - Send the message to the server.
   - Wait for an acknowledgment from the server.
4. The server will receive the message, verify its integrity, and respond with an acknowledgment.

5. To exit the client, type `'q'` and press **Enter**.

## Core Concept
- **UDP Communication**: Uses UDP sockets for connectionless communication between the client and server.
- **Message Encapsulation**: Messages are wrapped in a structured format, including:
  - Source and destination ports
  - Message length
  - Additional header fields
  - Checksum for integrity validation
- **Checksum Verification**: Implements a one's complement checksum to ensure data integrity during transmission.

## Preview of UDP Client-Server Communication

### **Client Side**
- The client prompts the user to enter a message.
- The message is encapsulated and sent to the server.
- The client receives an acknowledgment from the server.

### **Server Side**
- The server listens on port `12000` and waits for incoming messages.
- Upon receiving a message:
  - It extracts the header and validates the checksum.
  - If valid, it prints the received data and sends an acknowledgment.
  - If invalid, it notifies the client of a checksum error.

## Notes:
- This implementation ensures basic integrity checks through checksum verification.
- The system follows a structured message format for ease of parsing and debugging.
- Can be extended to support more complex network protocols or encryption mechanisms.

## Example Usage:
```bash
Client: Enter message (or 'q' to quit): Hello, Server!
Server: Received message with valid checksum.
Client: Received acknowledgment from server.
```
