
Target IP: 10.129.7.250

*Before Starting TMUX I make sure to export ip=10.129.7.250*

```bash
nmap -sC -sV $ip -oN initial.nmap
```

```plaintext
Starting Nmap 7.93 ( https://nmap.org ) at 2023-12-26 18:45 GMT
Nmap scan report for 10.129.7.250
Host is up (0.010s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT    STATE SERVICE       VERSION
80/tcp  open  http          Microsoft IIS httpd 10.0
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| http-title: Support Login Page
|_Requested resource was login.php
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
135/tcp open  msrpc         Microsoft Windows RPC
445/tcp open  microsoft-ds?
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2023-12-26T18:45:27
|_  start_date: N/A
| smb2-security-mode: 
|   311: 
|_    Message signing enabled but not required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
```

/login.php
![Heist Login Page](Screenshots\20231226135434.png)

**After clicking on the "Login as Guest" button we are redirected to /issues.php.**

/issues.php
![Heist Issues Page](Screenshots\20231226140232.png)

**Clicking on the "Attachment" in the issues comment takes us to /attachments/config.txt**

/attachments/config.txt
![Heist Issues Page](Screenshots\20231226140456.png)


**Fuzzing for directories gives us the following information**
```bash
ffuf -w /usr/share/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ  -u "http://$ip:80/FUZZ" -s
```

```plaintext
Images
css
js
attachments
IMAGES
CSS
JS
Attachments
```


```
security passwords min-length 12
enable secret 5 $1$pdQG$o8nrSzsGXeaduXrjlvKc91
!
username rout3r password 7 0242114B0E143F015F5D1E161713
username admin privilege 15 password 7 02375012182C1A1D751618034F36415408
```

SUPPORTDESK\hazard:stealth1agent

Now I’ll try with the credentials I’ve gathered. [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec/wiki/Using-Credentials) is a great tool here. I can give it a list of username and passwords, and let it tell me which one worked:
'
'
Potential Users
- support admin
- Hazard