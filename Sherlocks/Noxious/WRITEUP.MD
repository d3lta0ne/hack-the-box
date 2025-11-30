# HTB Write-Up: Noxious

![BOX Screenshot](https://htb-mp-prod-public-storage.s3.eu-central-1.amazonaws.com/challenges/8d317bdcf4aafcfc22149d77babee96d.png)

## Table of Contents

1. [Challenge Overview](#challenge-overview)
2. [Guided Questions](#guided-questions)
    - [1. Find the Malicious IP Address](#1-find-the-malicious-ip-address)
    - [2. Hostname of the Rogue Machine](#2-hostname-of-the-rogue-machine)
    - [3. Username Whose Hash Was Captured](#3-username-whose-hash-was-captured)
    - [4. When Were the Hashes Captured the First Time](#4-when-were-the-hashes-captured-the-first-time)
    - [5. Victim's Typo When Navigating to File Share](#5-victims-typo-when-navigating-to-file-share)
    - [6. NTLM Server Challenge Value](#6-ntlm-server-challenge-value)
    - [7. NTProofStr Value](#7-ntproofstr-value)
    - [8. Recovering the Password](#8-recovering-the-password)
    - [9. Actual File Share Accessed](#9-actual-file-share-accessed)
7. [Conclusion](#conclusion)

---

## Challenge Overview

- **Name**: Noxious
- **Category**: Sherlock
- **Difficulty**: Very Easy
- **Description**: 
    The IDS device alerted us to a possible rogue device in the internal Active Directory network. The Intrusion Detection System also indicated signs of LLMNR traffic, which is unusual. It is suspected that an LLMNR poisoning attack occurred. The LLMNR traffic was directed towards Forela-WKstn002, which has the IP address 172.17.79.136. A limited packet capture from the surrounding time is provided to you, our Network Forensics expert. Since this occurred in the Active Directory VLAN, it is suggested that we perform network threat hunting with the Active Directory attack vector in mind, specifically focusing on LLMNR poisoning.
- **Created By**: CyberJunkie
- **Date**: [08/01/2024]

## Initial Analysis :

## Guided Questions

1. It's suspected by the security team that there was a rogue device in Forela's internal network running the responder tool to perform an LLMNR Poisoning attack. Please find the malicious IP Address of the machine.
2. What is the hostname of the rogue machine?
3. Now we need to confirm whether the attacker captured the user's hash and if it is crackable. What is the username whose hash was captured?
4. In NTLM traffic, we can see that the victim credentials were relayed multiple times to the attacker's machine. When were the hashes captured the first time?
5. What was the typo made by the victim when navigating to the file share that caused his credentials to be leaked?
6. To get the actual credentials of the victim user, we need to stitch together multiple values from the NTLM negotiation packets. What is the NTLM server challenge value?
7. Now, doing something similar, find the NTProofStr value.
8. To test the password complexity, try recovering the password from the information found from the packet capture. This is a crucial step, as this way we can find whether the attacker was able to crack this and how quickly.
9. Just to get more context surrounding the incident, what is the actual file share that the victim was trying to navigate to?

## Conclusion

## Sample Table

| Name          | Age | Occupation        | Location      |
| ------------- | --- | ----------------- | ------------- |
| John Doe      | 29  | Software Engineer | New York      |
| Jane Smith    | 34  | Data Scientist    | San Francisco |
| Alice Johnson | 25  | UX Designer       | London        |
| Bob Brown     | 40  | Product Manager   | Berlin        |
