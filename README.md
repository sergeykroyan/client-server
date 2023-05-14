# Client-Server

This project is a Python implementation of a client-server architecture, showcasing the use of three different algorithms. The server acts as a central hub, receiving requests from clients and processing them using the specified algorithms. The clients can connect to the server, send data, and receive the processed results.

## Features

- Client-Server communication using sockets.
- Three algorithms implemented on the server:
  1. Affine Cipher: A substitution cipher that combines the functions of the Caesar cipher with modular arithmetic to encrypt and decrypt messages.
  2. RLE (Run-Length Encoding): A simple compression algorithm that replaces repeated consecutive characters with a count and the character itself.
  3. RSA (Rivest-Shamir-Adleman): A widely used asymmetric encryption algorithm for secure data transmission and digital signatures, based on the mathematical properties of large prime numbers.

## Requairments

- Python 3.7 or higher.


## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/sergeykroyan/client-server.git

2. Once you have cloned the repository and want to create a virtual environment, you can do so by running the command.
```sh
python -m venv env
```
3. After this, it's necessary to activate the virtual environment.

## Usage

1. Start the server by running the following command:

   ```shell
   python server.py
   
  The server will start and listen for incoming connections on the specified port.

2. Run the client by executing the following command:
   ```shell
   python client.py
  The client will connect to the server and prompt you to enter the data to be processed.

3. Follow the prompts on the client-side to send data and receive processed results.

