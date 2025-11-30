# HTB Write-Up: Global Hyperlink Zone (https://app.hackthebox.com/challenges/Global%20Hyperlink%20Zone)


## Table of Contents

1. [Challenge Overview](#challenge-overview)
2. [Methodology](#methodology)
3. [Answer](#answer)
4. [Conclusion](#conclusion)

---

## Challenge Overview

- **Name**: Global Hyperlink Zone
- **Category**: Web
- **Difficulty**: Easy
- **Description**: Beneath Qubitrix’s corporate towers lies the Global Hyperlink Zone - their prototype quantum internet. Its five access nodes authenticate through specific quantum gate patterns. Retrieve the sequence, stabilize the hyperlink, and force entry into their hidden backbone. One wrong move, and the link collapses.
- **Created By**: DCryp7
- **Date**: 11/29/2025

---

| Acronym     | Meaning                                                 |
| :---------- | :------------------------------------------------------ |
| TARGET_IP   | Spawned Target Machine IP Address                       |
| TARGET_PORT | Spawned Target Machine Port                             |
| PMN_BOX     | Personal Machine with a Connection to the Academy's VPN |
| PWN_IP      | Pwnbox IP Address (or PMVPN IP Address)                 |
| PWN_PORT    | Pwnbox Port (or PMVPN Port)                             |

---

Remember to uncompress the zip file using the password: `hackthebox` and the SHA-256 hash is: `0e77e3505e3020bfac6e59d4d2f1d247022a09bf6f8fdc1be07f3d56de2b405a`


## Methodology

Navigate to the http://TARGET_IP:TARGET_PORT and you are greeted with a server 404 page that states "Error, Cannot GET /".

![404 Response](../screenshots/404.png)

Looking into the actual request we say that we are gettting a `404 Not Found` error, from an Express Server.

![404 Response](../screenshots/404-response.png)

## Answer

### Flag

```
HTB{ROOT}
```

## Conclusion
