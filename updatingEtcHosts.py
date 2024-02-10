import sys
import ctypes
import platform

# Define the path of the hosts file based on the OS
if platform.system() == 'Windows':
    hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
else:
    hosts_path = '/ect/hosts'


def disclaimer():
    print("\nThis code has only been test on a Windows device."
          "\nIF YOU DON'T HAVE ADMIN PRIVILEGES this code will open a new"
          "\nwindow as administrator. You will need to run the same option 3"
          "\nand then continue from there.  You have to have admin rights"
          "\nto edit this file. I would then close that window and continue here"
          "\nYou probably shouldn't be trusted using the admin terminal")


def add_to_hosts_file(ip_address, hostname):
    try:
        with open(hosts_path, 'a') as file:
            file.write(f"\n{ip_address}\t{hostname}")
        print(f"Added {ip_address} {hostname} to hosts file.")
    except PermissionError:
        print("Permission denied. Run the script with elevated privileges.")


# Function to check if script is running with administrative privileges on Windows
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# Function to run the hosts file modification with elevated privileges
def run_with_elevated_privileges():
    user_choice = input("\nWould you like to enter a custom IP and hostname? (y/n): ")
    if user_choice.lower() == 'y':
        ip_address = input("Enter IP address: ")
        hostname = input("Enter hostname: ")
    else:
        print("\nUsing default...")
        ip_address = '10.10.11.130'
        hostname = 'internal-administration.goodgames.htb'
    if platform.system() == 'Windows' and not is_admin():
        print("Attempting to elevate privileges...\n")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        add_to_hosts_file(ip_address, hostname)
        print("\nYour /etc/hosts file has been updated with the ip address and hostname\n")  # Modify hosts file
