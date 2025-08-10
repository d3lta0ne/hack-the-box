#!/bin/bash

export writeup=$PWD;

#############################

# Set your variables
export TARGET="value1"
export TARGET_IP="10.10.11.58"
export PORT="value3"
export DOMAIN="value4"
export WORDLIST="value4"
export OUTPUT_FILE="/files/nmap/initial"

# Create DNS names for the `$TARGET_IP` in `/etc/hosts`.
#echo '$DOMAIN $TARGET_IP' | sudo tee -a /etc/hosts

# Create an environment variable of open ports using nmap
# export PORTS=$(nmap -p- --min-rate=1000 -T4 $TARGET_IP | grep '^[0-9]' | cut -d '/' -f 1 | tr '\n' ',' | sed s/,$//)

# Create a file of the currently open ports
# echo $PORTS > open_ports.txt 

# Create nmap output of all open ports
# sudo nmap -sC -sV -p$PORTS -vvv $TARGET_IP -oA $OUTPUT_FILE

# Ensure that URL Encode has already been installed on your system
# TARGET_IP=$(echo "$TARGET_IP" | urlencode) 