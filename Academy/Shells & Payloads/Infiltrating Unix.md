Author: d3lta0n3
Date: !TODO

# Setup
1. Create enviornmental variables from information generated for the machine.

```bash
export TARGET_IP=127.0.0.1
export TARGET_PORT=80
export PWN_IP=10.0.0.1
export PWN_PORT=12346
```

2. Create DNS names for the `$TARGET_IP` in `/etc/hosts`.

```bash
echo 'TARGET_IP $TARGET_IP' | sudo tee -a /etc/hosts
```

3. Run NMAP against `$TARGET_IP`. Remember that `$PORTS` is a list of all open ports on the machine.

```bash
# Create an environment variable of open ports using nmap
export PORTS=$(nmap -p- --min-rate=1000 -T4 $TARGET_IP | grep '^[0-9]' | cut -d '/' -f 1 | tr '\n' ',' | sed s/,$//)
```

```bash
# Create a file of the currently open ports
echo $PORTS > open_ports.txt 
```

```bash
# Nmap Syntax
sudo nmap -sC -sV -p$PORTS -vvv $TARGET_IP  -oA $OUTPUT_FILE
```

# Problem
[BOX Image Screenshot]()

|Acronym| 	Meaning|
|-----|---------|
|TARGET_IP| 	Spawned Target Machine IP Address|
|TARGET_PORT| 	Spawned Target Machine Port|
|PMN_BOX| 	Personal Machine with a Connection to the Academy's VPN|
|PWN_IP| 	Pwnbox IP Address (or PMVPN IP Address)|
|PWN_PORT| 	Pwnbox Port (or PMVPN Port)|

# Methodology
## Enumeration


# Solution
## User Flag
## Root Flag