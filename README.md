# SSH Honeypot

This project is a simple SSH honeypot designed to log authentication attempts and gather geolocation data of the connecting clients. It uses the `paramiko` library to simulate an SSH server and logs connection details for analysis.


## Screenshot of logs:
<img src=./src/image.png>

## Features

- Simulates an SSH server
- Logs connection attempts with username and password
- Retrieves and logs geolocation data of the connecting clients (requires IPINFO API key)
- Multi-threaded to handle multiple connections simultaneously

## Requirements

- Python 3.12
- `paramiko` library
- `requests` library
- `python-dotenv` library

## Setup

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the environment variables:**

    Create a `.env` file in the root directory and add your IPINFO API key:

    ```env
    GEO_API_KEY=your_ipinfo_api_key
    ```

## Usage

1. **Run the SSH honeypot:**

    ```sh
    python main.py
    ```

2. **Check the logs:**

    Connection attempts and geolocation data are logged in `ssh_server.log`.

## Code Overview

- `main.py`: Contains the main logic for the SSH honeypot.
  - `createRSAKey()`: Generates an RSA key for the SSH server.
  - `get_location(ip)`: Retrieves geolocation data for the given IP address.
  - `SSHServer`: A class that implements the `paramiko.ServerInterface` to handle SSH authentication.
  - `handle_connection(client_sock, client_addr)`: Handles incoming connections and starts the SSH server.
  - `main()`: Sets up the server socket and listens for incoming connections.

