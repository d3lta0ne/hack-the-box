#!/bin/bash

# Set working directory to current writeup folder
export writeup="$PWD"

#############################
# Required variables (edit as needed)
export TARGET="example-machine"
export TARGET_IP="10.10.10.10"
export PORT="80"
export DOMAIN="example.htb"
export WORDLIST="/usr/share/wordlists/rockyou.txt"
export OUTPUT_FILE="$writeup/files/nmap/initial"

#############################
# Optional Enhancements

# Add domain to /etc/hosts for resolution
# echo "$TARGET_IP $DOMAIN" | sudo tee -a /etc/hosts

# Scan for open ports and export as PORTS
# export PORTS=$(nmap -p- --min-rate=1000 -T4 $TARGET_IP | grep '^[0-9]' | cut -d '/' -f 1 | tr '\\n' ',' | sed 's/,\$//')

# Save open ports to file
# echo "$PORTS" > "$writeup/open_ports.txt"

# Run full Nmap scan and save output
# sudo nmap -sC -sV -p"$PORTS" -vvv $TARGET_IP -oA "$OUTPUT_FILE"

# URL encode the target IP (requires 'urlencode' installed)
# TARGET_IP=$(echo "$TARGET_IP" | urlencode)
