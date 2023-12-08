import re
import subprocess
import socket
import ipaddress

__version__ = '1.0.0'
__author__ = 'Teeraphat Kullanankanjana'

class TelloIPScaner:
    def __init__(self, target=None, subnet="/24", debug=True):
        self.subnet = subnet
        self.debug = debug
        if target is None:
            # If target is not provided, get the local IP address with /24 subnet
            self.target = self.get_local_ip()
        else:
            self.target = target

    def get_local_ip(self):
        # Use socket to get the local IP address
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Connect to a known external server
            local_ip = s.getsockname()[0]
        except socket.error as e:
            print("Error getting local IP:", e)
            local_ip = "127.0.0.1"  # Default to loopback address if an error occurs
        finally:
            s.close()

        # Create an IPv4 network with a /24 subnet based on the obtained local IP
        local_network = ipaddress.IPv4Network(f"{local_ip}{self.subnet}", strict=False)
        return str(local_network)

    def run_scan(self):
        nmap_command = ["nmap", "-sn", self.target]
        print("Scanning...")

        try:
            result = subprocess.run(
                nmap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
            )
            nmap_output = result.stdout

            pattern = r"Nmap scan report for (\d+\.\d+\.\d+\.\d+)\nHost is up \(([\d.]+)s latency\)\.\nMAC Address: ([\dA-Fa-f:]+) \((SZ DJI Technology)\)"

            matches = re.findall(pattern, nmap_output)
            if not matches:
                print("Not Found")
                return

            for match in matches:
                ip_address, latency, mac_address, manufacturer = match
                if self.debug:
                    print(f"IP Address: {ip_address}, MAC Address: {mac_address}, Manufacturer: {manufacturer}, Latency: {latency}")
                else:
                    print(f"IP Address: {ip_address}")

        except subprocess.CalledProcessError as e:
            print("Error running Nmap:", e)
            print("Nmap Output (stderr):")
            print(e.stderr)

if __name__ == "__main__":
    # Example usage without specifying IP address
    scanner = NmapScanner()
    scanner.run_scan()
