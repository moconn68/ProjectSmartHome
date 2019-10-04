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

[Link to Reference Source]<http://lewiscomputerhowto.blogspot.com/2014/06/how-to-hack-wpawpa2-wi-fi-with-kali.html>

## 3. Obtaining Root Machine Access via SSH Dictionary Attack

On Unix-based systems, the "root" user is one that has full administrative access and priviledges to all resources on the computer. This provides a high level of capability and customizability, but can be a massive security risk if the wrong person were able to gain root access. In this scenario, we will use a dictionary attack based on a large list of data in order to crack the root password on our Smart Home model.

1. Connect to the same network as the Smart Home. In this case, it is the network for the Onion Omega2. If you have not yet determined the password, obtain it by following scenario 2 above. 
2. To obtain the IP address of the device we want to connect to, in this case the Onion Omega2 powering our Smart Home, run `ifconfig` to determine the internet IP address followed by `sudo nmap -sn <nwk ip>/24` to scan for all IPs connected to the network. Search the output for anything with "Omega" and note its IP address. It should be 192.168.3.1
3. This dictionary attack requires two lists; one for usernames and one for passwords. Since we know we are searching only for the root password, we only need "root" as a username. Create a new file on your Desktop called "users.txt" and put `root` as its only contents.
4. For the list of passwords, you can try out any in the /usr/shared/wordlists/ directory, but as in step 2 we will use the one located at /usr/share/wordlists/dirb/big.txt . If this does not work for you feel free to experiment with others or download new ones from the internet.
5. To begin the attack via SSH, use the hydra command: `hydra -L /root/Desktop/users.txt -P /usr/share/wordlists/dirb/big.txt <Onion IP> ssh` . This will take some time, and may be unsuccessful. Keep trying with multiple password lists.
6. Once the attack is successful and the password is cracked, search the output for the cracked password. Try to log into the Smart Home using ssh: `ssh root@<Onion IP>` and then when prompted enter the password. If this works, congratulations! You now have root access to the Smart Home and may do anything you please.

[Link to Reference Source]<https://www.hackingarticles.in/6-ways-to-hack-ssh-login-password/>
 
