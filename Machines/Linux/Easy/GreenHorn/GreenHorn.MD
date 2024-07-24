Author: d3lta0n3
Date: 7/23/2024


# Setup


1. Create enviornmental variables from the Target IP Address that is generated for the machine.

```bash
export TARGET_IP=10.129.134.162
export TARGET_PORT=80
export PWN_IP=10.10.14.14
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
sudo nmap -sC -sV -p$PORTS -vvv $TARGET_IP  -oA green-horn
```

# Problem
![HTB GreenHorn Screenshot Cover](Screenshots\green-horn_cover.png)

|Acronym| 	Meaning|
|-----|---------|
|TARGET_IP| 	Spawned Target Machine IP Address|
|TARGET_PORT| 	Spawned Target Machine Port|
|PMN_BOX| 	Personal Machine with a Connection to the Academy's VPN|
|PWN_IP| 	Pwnbox IP Address (or PMVPN IP Address)|
|PWN_PORT| 	Pwnbox Port (or PMVPN Port)|

# Methodology


## Enumeration
We start by opening `tmux` after setting up our environmental variables and running an nmap scan on the target.

```nmap

PORT     STATE SERVICE REASON         VERSION
22/tcp   open  ssh     syn-ack ttl 63 OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    syn-ack ttl 63 nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://greenhorn.htb/
3000/tcp open  ppp?    syn-ack ttl 63

<SNIP>
```

After going through [green-horn.nmap](Files/green-horn.nmap), we find out that the box is expecting to redirect to `http://greenhorn.htb/`. Thus, we add this hostname to our `/etc/hosts` file and proceed with enumeration of the target on ports 80 and 3000. We retrict searching port 22 as we have no credentials or information to spray with.

```bash
echo "$TARGET_IP greenhorn.htb" | sudo tee -a /etc/hosts
```

We see that at the bottom of the [Home Page](http://greenhorn.htb/?file=welcome-to-greenhorn) that their is an admin page and that the backend CMS is `plunk`. This redirects us to the [Admin Page](http://greenhorn.htb/login.php). We can't find any default credentials for the Plunk CMS but take note that we are using `pluck 4.7.18`. This version is tied directly to an [Exploit](https://www.exploit-db.com/exploits/51592) that we will use later.

This pushes us to pivot to enumerating the PPP service on port 3000. We are taken to a Github-like service that seems to host the files for the HTTP server on port 80. We find a [GreenHorn Repo](http://greenhorn.htb:3000/GreenAdmin/GreenHorn) with the description that "We believe in open source.". Looking at the `login.php` file, we see very interesting information about the authentication method on lines 38-48.

/login.php
```php
//If pluck is installed:
else {
	require_once 'data/settings/pass.php';

	//Check if we're already logged in. First, get the token.
	require_once 'data/settings/token.php';

	if (isset($_SESSION[$token]) && ($_SESSION[$token] == 'pluck_loggedin')) {
		header('Location: admin.php');
		exit;
	}
```

This information disclosure indicates that we can find information about the admin password and token in the respective `data/settings/pass.php` and `data/settings/token.php` files.

/data/settings/pass.php
```php
<?php
$ww = 'd5443aef1b64544f3685bf112f6c405218c573c7279a831b1fe9612e3a4d770486743c5580556c0d838b51749de15530f87fb793afdcc689b6b39024d7790163';
?>
```

This `$ww` variable, appears to be a hash and we will save it and attempt to break it with hashcat as follows. We save it into a `hash` file and then pass it to hashid to better identify it.

```bash
echo 'd5443aef1b64544f3685bf112f6c405218c573c7279a831b1fe9612e3a4d770486743c5580556c0d838b51749de15530f87fb793afdcc689b6b39024d7790163' > hash
hashid hash -m
```

### Ports

#### Port: 22 (SSH)


#### Port: 80  (HTTP)

URL: http://greenhorn.htb/?file=welcome-to-greenhorn

![GreenHorn Splash Page](Screenshots\green-horn_dashboard.png)

URL: http://greenhorn.htb/login.php

![GreenHorn Admin Page](Screenshots\green-horn_admin.png)

#### Port: 3000 (PPP)

URL: http://greenhorn.htb:3000/

![GreenHorn Port 3000](Screenshots\green-horn_3000.png)

We 

# Solution


## User Flag


## Root Flag


# Footnotes


