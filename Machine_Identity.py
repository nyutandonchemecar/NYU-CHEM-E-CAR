import platform
import socket
import psutil
import os

def get_system_info():
    # Get hostname and IP
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip_address = "Unable to retrieve IP"

    print("========== System Information ==========")
    print(f"Hostname: {hostname}")
    print(f"IP Address: {ip_address}")
    print(f"System: {platform.system()}")
    print(f"Machine Type: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"CPU Cores (Physical): {psutil.cpu_count(logical=False)}")
    print(f"CPU Threads (Logical): {psutil.cpu_count(logical=True)}")
    print(f"OS Version: {platform.version()}")
    print(f"OS Release: {platform.release()}")
    print(f"Architecture: {platform.architecture()[0]}")
    print(f"Python Version: {platform.python_version()}")

    # RAM info
    ram = psutil.virtual_memory()
    print("\n========== Memory Information ==========")
    print(f"Total RAM: {ram.total / (1024 ** 3):.2f} GB")
    print(f"Available RAM: {ram.available / (1024 ** 3):.2f} GB")
    print(f"Used RAM: {ram.used / (1024 ** 3):.2f} GB")
    print(f"RAM Usage: {ram.percent}%")

    # Disk info
    print("\n========== Disk Information ==========")
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"Drive: {partition.device}")
            print(f"  Mountpoint: {partition.mountpoint}")
            print(f"  File system: {partition.fstype}")
            print(f"  Total Size: {usage.total / (1024 ** 3):.2f} GB")
            print(f"  Used: {usage.used / (1024 ** 3):.2f} GB")
            print(f"  Free: {usage.free / (1024 ** 3):.2f} GB")
            print(f"  Usage: {usage.percent}%")
        except PermissionError:
            continue

    print("\n========================================")

if __name__ == "__main__":
    get_system_info()
