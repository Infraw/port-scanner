import socket
from termcolor import colored
import argparse
import os

# Parser
parser = argparse.ArgumentParser(description="Infraw's Port Scanner")

# Arguments
parser.add_argument('host', type=str, help='The target host to scan')
parser.add_argument('start_port', type=int, help='The starting port')
parser.add_argument('end_port', type=int, help='The ending port')

args = parser.parse_args()

# Variables
host = args.host
start_port = args.start_port
end_port = args.end_port

# ICMP echo request
response = os.system("ping -c 4 " + host)
if response == 0:
    print(colored(host + " is available.", 'green'))
else:
    print(colored(host + " is cannot reachable\nExiting", 'red'))
    exit()

# Counters
open_sockets = 0
closed_sockets = 0
open_ports = []

# Iterate over ports
for port in range(start_port, end_port+1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        if result == 0:
            open_sockets += 1
            open_ports.append(port)
            print(colored(f"Port {port} is open", 'green'))
        else:
            closed_sockets += 1
            print(colored(f"Port {port} is closed", 'red'))
        sock.close()
    except socket.timeout:
        print(colored(f"Connection to port {port} timed out", 'yellow'))
    except socket.error:
        print(colored("Could not connect to server. Exiting", 'red'))
        exit()

#Write open ports if there are any
if open_sockets > 0:
    with open("open_ports.txt", "w") as f:
        for port in open_ports:
            f.write(str(port) + "\n")
    print(colored("Open ports were written to open_ports.txt", 'green'))
else:
    print(colored("No open ports were found", 'red'))

#Results
print(colored(f"Scan complete: {open_sockets} open sockets, {closed_sockets} closed sockets", 'cyan'))
