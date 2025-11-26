# HTB Write-Up: [Outbound](https://app.hackthebox.com/machines/Outbound)

![BOX Screenshot](../screenshots/oubound-logo.png)

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

- **Name**: Outbound
- **Category**: Linux
- **Difficulty**: Easy
- **Description**: 
     `Outbound` is an easy-difficulty Linux machine with provided assumed breach credentials. The credentials provide access to a `Roundcube` instance, where the user can enumerate the version and utilize [CVE-2025-49113](https://nvd.nist.gov/vuln/detail/CVE-2025-49113), which demonstrates post-authenticated remote code execution via PHP object deserialization. After initial access to the target, we enumerate the database and find a session for the Jacob user, which, when base64 decoded, provides an encrypted password. Using an internal tool called `decrypt.sh`, we can extract the plaintext value of the password, which allows access to Roundcube as Jacob. Jacob has two messages in his inbox: one provides him with a new, updated password for the system, and another informs him that they have been granted `sudo` privileges to monitor system resources with a utility called `below` which is vulnerable to [CVE-2025-27591](https://nvd.nist.gov/vuln/detail/CVE-2025-27591) that is a flaw that creates logs within the `/var/log/below` directory with excessive permissions allowing attackers to perform symlink attacks under certain conditions. We symlink `/etc/passwd` to the `error_root.log` file and write our payload to the log file via parameter injection, thereby creating a new user with a UID of the root user. 
- **Created By**: TheCyberGeek
- **Writeup Date**: 26 Nov 2025

---

| Acronym     | Meaning                                                 |
| :---------- | :------------------------------------------------------ |
| TARGET_IP   | Spawned Target Machine IP Address                       |
| TARGET_PORT | Spawned Target Machine Port                             |
| PMN_BOX     | Personal Machine with a Connection to the Academy's VPN |
| PWN_IP      | Pwnbox IP Address (or PMVPN IP Address)                 |
| PWN_PORT    | Pwnbox Port (or PMVPN Port)                             |

---

## Methodology

## Information Gathering

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
