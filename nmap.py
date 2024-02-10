import subprocess
import re

nmap_flags = {
    "1": "-sS (Check if key ports are open)",
    "2": "-sT (Check if you can establish a connection)",
    "3": "-sU (Scan UDP ports instead of default TCP)",
    "4": "-sY (Scan for SCTP ports specifically)",
    "5": "-sN/-sF/-sX (Special scans for sneaky ports)",
    "6": "-sV (Get service and application versions running)",
    "7": "-O (Try to figure out OS from little clues)",
    "8": "-sC (Use some smart premade scripts)",
    "9": "-v (Show me more details as it scans)",
    "10": "default"
}


def run_nmap(ip_address):
    print("Select Nmap flags to use (enter numbers separated by spaces):")

    for key, value in nmap_flags.items():
        print(f"{key}. {value}")

    selections = input("> ")
    selected_flags = [nmap_flags[x] for x in selections.split()]

    flags = " ".join(selected_flags)

    nmap_path = r'C:\\Program Files (x86)\\Nmap\\nmap.exe'
    if flags == 'default':
        command = f'"{nmap_path}" -sC -sV --unprivileged {ip_address}'
    else:
        command = f'"{nmap_path}" {flags} --unprivileged {ip_address}'

    print("\nScanning IP with selected flags: \n")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, _ = process.communicate()
    return output


def extract_service_info(output):
    pattern = r'(\d+\/tcp)\s+(\w+)\s+(.+)'  # Regex pattern to match port, state, and service version
    matches = re.findall(pattern, output)
    results = ""

    for match in matches:
        results += f"Port: {match[0]}, State: {match[1]}, Service: {match[2]}"
        if match[0] == '80/tcp':
            results += ("\n\nWell it looks like you found an open port and"
                        "\nit looks like a typical http port. You should be"
                        "\nable to browse to the IP address through the browser\n")
    return results


# Replace this with your actual IP address
def run(ip='10.10.11.130'):
    target_ip = ip
    output = run_nmap(target_ip)
    result = extract_service_info(output)
    print(result)
