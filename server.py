import http.server
import socketserver
import socket
import os
import webbrowser
import subprocess
import sys
import time
from datetime import datetime

# Configuration
PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_local_ip():
    """Dynamically get the local IP address"""
    try:
        # Create a socket to get the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        # Fallback method
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except:
            return "127.0.0.1"

def get_hostname():
    """Get the computer name"""
    return socket.gethostname()

def save_ip_to_file(ip, hostname):
    """Save the IP address to a file for easy access"""
    with open(os.path.join(DIRECTORY, "server_info.txt"), "w") as f:
        f.write(f"Server running on:\n")
        f.write(f"Local IP: http://{ip}:{PORT}\n")
        f.write(f"Hostname: http://{hostname}:{PORT}\n")
        f.write(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Directory: {DIRECTORY}\n")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler with logging"""
    def log_message(self, format, *args):
        """Add timestamp to log messages"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")

def start_server():
    """Start the HTTP server"""
    # Change to the directory containing the HTML files
    os.chdir(DIRECTORY)
    
    # Get dynamic IP
    ip = get_local_ip()
    hostname = get_hostname()
    
    # Save IP info
    save_ip_to_file(ip, hostname)
    
    # Print server information
    print("=" * 60)
    print(f"🚀 Stark Expo Server Started")
    print("=" * 60)
    print(f"📁 Serving: {DIRECTORY}")
    print(f"🌐 Local IP: http://{ip}:{PORT}")
    print(f"🖥️  Hostname: http://{hostname}:{PORT}")
    print(f"📱 Access from other devices on the same network")
    print(f"📋 IP saved to: server_info.txt")
    print("=" * 60)
    print("Press Ctrl+C to stop the server\n")
    
    # Open browser automatically
    try:
        webbrowser.open(f"http://{ip}:{PORT}")
    except:
        pass
    
    # Start the server
    handler = CustomHandler
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            httpd.shutdown()

def stop_server():
    """Stop the server by killing the process on port 8000"""
    print("🛑 Stopping server on port 8000...")
    try:
        # Find and kill the process using port 8000
        result = subprocess.run(
            f'netstat -ano | findstr :{PORT} | findstr LISTENING',
            shell=True,
            capture_output=True,
            text=True
        )
        
        for line in result.stdout.split('\n'):
            if line.strip():
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    try:
                        subprocess.run(f'taskkill /F /PID {pid}', shell=True, capture_output=True)
                        print(f"✅ Killed process with PID: {pid}")
                    except:
                        pass
        print("✅ Server stopped")
    except Exception as e:
        print(f"❌ Error stopping server: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stop":
        stop_server()
    else:
        start_server()