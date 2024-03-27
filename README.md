# Project Title
Digital Twins of Cyber-Physical Systems in Smart Manufacturing: Threat Simulation and Detection via Deep Learning for Time Series Classification

# Project Aim
Our research aims to overcome the limitations of physical testbeds and challenges of data scarcity for Machine Learning (ML) or Deep Learning (DL) model development. 

By leveraging Digital Twins for data-driven analysis, this study proposes the use of supervised DL techniques for accurate threat detection and classification in CPS within smart manufacturing. 

# Overview of the Digital Twins Testbed Setup

This GitHub repository provides an overview of setting up the Digital Twins testbed. The setup guide enables the cybersecurity community to replicate and broaden our methodology, thus enhancing security measures in smart manufacturing ecosystems.

## Hardware and Software Required

You will need the following hardware and software for setting up the Digital Twins testbed:

- [Factory I/O 3D Simulator](https://factoryio.com/) (30-day free trial of Ultimate Edition, the monthly licence fee for Ultimate Edition is €28. There are many [readily made scene in Factory I/O](https://docs.factoryio.com/getting-started/opening-a-scene/). This project build a quality checking scene from scratch.)

- [OpenPLC Programmable Logic Controller Simulator](https://autonomylogic.com/)) (completely free of charge. Thanks Dr. Thiago Alves for providing a low cost industrial PLC for automation and research.)

- [Raspberry Pi](https://www.raspberrypi.com/products/) for hosting OpenPLC (At the moment, Raspberry Pi 4 is the most stable for OpenPLC, it costs around £60. OpenPLC is yet to work on Raspberry Pi 5 due to dependency on [WiringPi](https://github.com/WiringPi/WiringPi). If you like, you could also use other microcontrollers such as Arduino to set up the PLC simulator with OpenPLC. Another option is using [industrial grade PLC](https://docs.factoryio.com/getting-started/controlling-with-a-plc/), such as those manufactured by Siemens, Allen-Bradley, to replace OpenPLC but it would be comparatively expensive than using OpenPLC)

## Installation and setup guide

### (a) Setup OpenPLC on Raspberry Pi
1) Install and run Raspberry Pi OS ([Debian Bullseye with Raspberry Pi Desktop](https://www.raspberrypi.com/software/operating-systems/) on Raspberry Pi 4 
2) Install and setup OpenPLC Runtime on Raspberry Pi 4. Refer to [installation manual](https://autonomylogic.com/docs/installing-openplc-runtime-on-linux-systems/) and [OpenPLC YouTube videos](https://www.youtube.com/@openplc/videos) for explanation. Refer to [settings for Slave Device on OpenPLC](OpenPLCSlave.png) for more details.
3) Unzip [Factory I/O Runtime File](FactoryIO_E1.zip), upload the program named 655575.st onto OpenPLC Runtime.

### (b) Setup Factory I/O 
1) Install and run Factory I/O on computer that meets the [system requirement](https://factoryio.com/start-trial)
2) Open the [quality checking scene](FactoryIOE1.factoryio)
3) Start the connection and run the file. Refer to the [UWECyber YouTube playlist](https://www.youtube.com/playlist?list=PLqaj1AbWsq7ueS2nn_PImJG2-4CWEPxNQ) if you want to learn more about how to run your own Factory I/O scenes.

# Threat simulation and data collection
