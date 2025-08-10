#!/bin/bash

export writeup=$PWD;

#############################
# I want to be able to provide an ip in the following options
- '10.0.0.1'
- '10.0.0.1/32'
- '10.0.0.1/24' #the whole range

# If i pass ipv4 prompt me to see if you should scan the ipv6 equivilent

# If i pass ipv6 only do commands for ipv6 stuff

# if the target is more than one host or is in a given range, create a file called targetlist.ip
export TARGET_LIST;

# Set your variables
export TARGET="value1"
export TARGET_IP="value2"
export PORT="value3"
export DOMAIN="value4"
export WORDLIST="value4"
export OUTPUT_FILE="/files/nmap/initial"

# Wordlist variables
# create a list of wordlist variables to save you time when passing username wordlist, password lists and more
export usernamelist=""
export passwordlist=""
export defaultusernamelist=""
export defaultpasswordlist=""
export domainenumlist=""
export vhostenumlist=""
## and more 

######### ask me if i want to do enumeration #####


### Enumeration Tools ###
- nmap # this runs the nmap enum stuff

# Create DNS names for the `$TARGET_IP` in `/etc/hosts`.
# echo '$DOMAIN $TARGET_IP' | sudo tee -a /etc/hosts

# IF RUN NMAP ENUMERATION SCANS
    ## Create a folder called nmap_scans
        - nmap_scans
            - host1
                - open_ports
                - filter_ports
                - syn.results.xml
            - host2

    ## use the following command to create an open_ports and a filter_ports file for each host 
    export OPEN_PORTS=$(nmap -p- --min-rate=1000 -T4 $TARGET_IP | grep '^[0-9]' | cut -d '/' -f 1 | tr '\n' ',' | sed s/,$//)
    echo $OPEN_PORTS > nmap_scans.host{?}.open_ports.txt
        # repeat this for filtered ports
        # create a list of open TCP ports, open UDP ports, repeat for filtered. Try to minimize the amount of times I have to run the scan and then just parse the intial scan to different files

    ## Then run the following NMAP Scans on each target but only at the provided ports you are passed in with open_ports.
        nmap -n -A -PN -p- -T Agressive $TARGET_IP -oX nmap.syn.results.xml 
        nmap -sU -PN -v -O -p 1-30000 -T polite $TARGET_IP > nmap.udp.results
        nmap -sV -PN -v -p 21,22,23,25,53,80,443,161 $TARGET_IP > nmap.version.results
        nmap -A -sS -PN -n --script:all -iL $TARGET_IP --reason
        grep "appears to be up" nmap_saved_filename | awk -F '{print $2}' | awk -F '{print $1}' > ip_list

## NMAP ULTRA AGGRESIVE SCAN
nmap -oA fullscan-aggressive.txt -T4 -vvv --max-rtt-timeout 300ms --max-retries 3 --host-timeout 30m --max-scan-delay 500ms -Pn -p- --version-intensity 1 -iL fullscan.txt
# More stealthy and complete option
    nmap -sT -Pn -p- --max-parallelism 1 --max-retries 0 --max-rtt-timeout 1000ms --max-hostgroup 1 -oX nmap_x.x.x.x-all_ports_slow.xml -iL x.x.x.x_Active_IPs.txt
# IF 
# Create nmap output of all open ports
# sudo nmap -sC -sV -p$PORTS -vvv $TARGET_IP -oA $OUTPUT_FILE

# Ensure that URL Encode has already been installed on your system
# TARGET_IP=$(echo "$TARGET_IP" | urlencode) 