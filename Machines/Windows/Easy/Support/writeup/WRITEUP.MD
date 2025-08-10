# HTB Write-Up: [Challenge/Box Name]

![BOX Screenshot](../files/support_screenshot.png)

## Table of Contents

1. [Challenge Overview](#challenge-overview)
2. [Reconnaissance](#reconnaissance)
3. [Exploitation](#exploitation)
4. [Post-Exploitation](#post-exploitation)
5. [Privilege Escalation](#privilege-escalation)
6. [Answer](#answer)
7. [Conclusion](#conclusion)

---

## Challenge Overview

- **Name**: Support
- **Category**: [Category Type]
- **Difficulty**: Easy
- **Description**: 
 Support is an Easy difficulty Windows machine that features an SMB share that allows anonymous authentication. After connecting to the share, an executable file is discovered that is used to query the machine&amp;amp;amp;amp;#039;s LDAP server for available users. Through reverse engineering, network analysis or emulation, the password that the binary uses to bind the LDAP server is identified and can be used to make further LDAP queries. A user called `support` is identified in the users list, and the `info` field is found to contain his password, thus allowing for a WinRM connection to the machine. Once on the machine, domain information can be gathered through `SharpHound`, and `BloodHound` reveals that the `Shared Support Accounts` group that the `support` user is a member of, has `GenericAll` privileges on the Domain Controller. A Resource Based Constrained Delegation attack is performed, and a shell as `NT Authority\System` is received. 
- **Created By**: 0xdf
- **Date**: [2/17/2025]

---

| Acronym     | Meaning                                                 |
| :---------- | :------------------------------------------------------ |
| TARGET_IP   | Spawned Target Machine IP Address                       |
| TARGET_PORT | Spawned Target Machine Port                             |
| PMN_BOX     | Personal Machine with a Connection to the Academy's VPN |
| PWN_IP      | Pwnbox IP Address (or PMVPN IP Address)                 |
| PWN_PORT    | Pwnbox Port (or PMVPN Port)                             |

---

## Initial Analysis :

## Questions (If it is guided)

1.
2.
3.

## Methodology (FOR NON-BOXES?)

## Reconnaissance

### Setup

1. Create enviornmental variables from information generated for the machine.

```bash
/bin/bash vars.bash
```

### Information Gathering

## Exploitation

## Post-Exploitation

## Privilege Escalation

## Enumeration

## Answer

### User Flag

```
HTB{USER}
```

### Root Flag

```
HTB{ROOT}
```

## Conclusion

## Sample Table

| Name          | Age | Occupation        | Location      |
| ------------- | --- | ----------------- | ------------- |
| John Doe      | 29  | Software Engineer | New York      |
| Jane Smith    | 34  | Data Scientist    | San Francisco |
| Alice Johnson | 25  | UX Designer       | London        |
| Bob Brown     | 40  | Product Manager   | Berlin        |
