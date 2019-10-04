# Project Smart Home

Villanova Engineering Senior Project Spring & Fall 2019

DiY Cyberphysical Systems

Preston Genett, Scott Panasci, Matthew O'Connell, Dominik Schab

# About

Project Smart Home, or more officially referred to as DiY Cyberphysical Systems (CPS), is our group's senior design project for our engineering capstone. The goal of this project is to create a scaled-down model of a common "cyberphysical system," or a system which contains both physical and digital components, for the purpose of cybersecurity training. While this concept has been explored before, our project takes this concept to new realms by increasing portability, functionality, educational efficacy, and wireless capability.

# Set-Up

Note that these steps are specific for connecting to an Omega2 configured for our project, not steps on how to set up and use an Onion Omega2 in general.

## Connecting to the Omega2

The Onion Omega2 is the System-on-a-Chip (SOC) powering this project. In order to access the software aspects of our model, you must use a direct WiFi connection to the Omega2.

1. Plug in & power on your Omega2
2. Go into your WiFi settings and connect to your Omega2's direct WiFi connection. It should be named "Omega-XXXX" where XXX = some combination of letters and/or numbers.
3. Open your browser of choice (**except for the Chromium open-source browser, although Chrome works fine**) and navigate to 192.168.3.1
4. Enter the username of root, and password of onioneer. This will log you into the Omega2's dashboard.

Once this project is completed, the end-products will be fully set-up and ready to go out of the box. These next steps detail the steps we used to configure our Onion Omega2 SOCs for development.

## Installing & Configuring Git

Although the Omega2 does come with git preinstalled, it lacks core functionality which we need in order to make effective use of it, primarily the ability to use HTTPS for data transfer. An additional problem is that at the time of this project, the Omega2 does not come preinstalled with `ssh-keygen`, so you actually cannot use SSH for Git either. This means that on first boot, you can only use git locally on your Omega2 which is a problem for much more than just this project.

1. [Follow this guide](https://docs.onion.io/omega2-docs/installing-and-using-git.html) in order to remedy the above problems.
2. Once your Git installation is completed, clone this repository to your Onion. You can do this anywhere, although the home directory is recommended for simplicity's sake.

## Importing the Node Red Code

Much of the workflow for this project is handled through IBM's Node Red platform, which at the time of development unfortunately is extremely lacking when it comes to version control as it is mostly a graphical system. However, it does have one method which involves importing and exporing the entirety of projects as JSON files. 

1. Add the node-red-dashboard module
2. Copy the contents of the file "NodeRed.txt" from within the project. Recommend to do this from the raw file on the GitHub repo as there can sometimes be weird copy-paste issues from the Omega2, at least on Linux.
3. Go into the Node Red dashboard in your browser and import a project from clipboard. Paste the text from step 2 into this box and click Import.

At this point, you should have access to all of the Node Red code. Click the red 'Deploy' button in the top right corner to deploy the code to the device and run it.

## Additional Modules and Functionality

There are some particular aspects of the model which require additional configuration of the Omega2:

+ [Complete these steps](https://onion.io/streaming-video-over-wifi/) in order to set up your onion for live video stream from a USB camera

# Using the Project

Once you have set up the model and configued the Onion Omega2 (if necessary), you are ready to use the project. In order to access the smart home dashboard, do the following:

1. Access the Node-Red application on your Onion
2. Open the side panel in the dashboard category
3. Click on the box in the top right corner of the menu to launch the dashboard

# License


This project is currently licensed under the GNU General Public License (GPL) Version 3. More information can be found within the LICENSE.md file.
