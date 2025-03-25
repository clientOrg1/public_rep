import requests
import argparse
import sys

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8000

def basic_hello_client(host, port):
    """Simple client that requests the /hello endpoint"""
    url = f"http://{host}:{port}/hello"
    try:
        response = requests.get(url)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")
        return False
    return True

def file_download_client(host, port, filename):
    """Client that downloads a file from the server"""
    url = f"http://{host}:{port}/{filename}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"downloaded_{filename}", "wb") as f:
                f.write(response.content)
            print(f"Successfully downloaded {filename}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")
        return False
    return True

def custom_request_client(host, port, path, method="GET"):
    """Custom client that can make different types of requests"""
    url = f"http://{host}:{port}{path}"
    try:
        if method.upper() == "GET":
            response = requests.get(url)
        elif method.upper() == "POST":
            response = requests.post(url, data={"test": "data"})
        elif method.upper() == "HEAD":
            response = requests.head(url)
        else:
            print(f"Unsupported method: {method}")
            return False
        
        print(f"Status code: {response.status_code}")
        if method.upper() != "HEAD":
            print(f"Response: {response.text}")
        print(f"Headers: {response.headers}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='HTTP client for server communication')
    parser.add_argument('--host', default=DEFAULT_HOST, help=f'Server hostname (default: {DEFAULT_HOST})')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help=f'Server port (default: {DEFAULT_PORT})')
    parser.add_argument('--mode', choices=['hello', 'download', 'custom'], default='hello',
                        help='Client mode (default: hello)')
    parser.add_argument('--file', help='Filename to download (for download mode)')
    parser.add_argument('--path', default='/hello', help='Request path (for custom mode)')
    parser.add_argument('--method', default='GET', help='HTTP method (for custom mode)')
    
    args = parser.parse_args()
    
    if args.mode == 'hello':
        basic_hello_client(args.host, args.port)
    elif args.mode == 'download':
        if not args.file:
            print("Error: --file argument is required for download mode")
            sys.exit(1)
        file_download_client(args.host, args.port, args.file)
    elif args.mode == 'custom':
        custom_request_client(args.host, args.port, args.path, args.method)