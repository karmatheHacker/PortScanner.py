# PortScanner.py
# Run the Script: Use the following command to run the script:
python portscanner.py <host> <start_port> <end_port> <timeout> [--verbose] [--output <file>]
<host>: The IP address or hostname of the target machine you want to scan.
<start_port>: The starting port number for the scan (e.g., 1).
<end_port>: The ending port number for the scan (e.g., 1024).
<timeout>: The timeout in seconds for each port scan (e.g., 1.0).
--verbose: (Optional) If included, the script will print detailed information about closed ports and errors.
--output <file>: (Optional) If included, the script will save the results to the specified file.
# Example Commands:
python portscanner.py example.com 1 1024 1.0
python portscanner.py 192.168.1.1 1 1024 1.0 --verbose
python portscanner.py example.com 1 1024 1.0 --output output.txt
