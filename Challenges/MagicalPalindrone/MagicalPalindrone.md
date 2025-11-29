# HTB Write-Up: Magical Palindrome (https://app.hackthebox.com/challenges/Magical%20Palindrome)

## Table of Contents

1. [Challenge Overview](#challenge-overview)
2. [Methodology](#methodology)
3. [Answer](#answer)

---

## Challenge Overview

- **Name**: MagicalPalindrone
- **Category**: Web
- **Difficulty**: Very Easy
- **Description**: In Dumbledore's absence, Harry's memory fades, leaving crucial words lost. Delve into the arcane world, harness the power of JSON, and unveil the hidden spell to restore his recollection. Can you help harry yo find path to salvation?
- **Created By**: Anekant
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
## Notes
Remember to uncompress the zip file using the password: `hackthebox` and the SHA-256 hash is: `e32b1381a68835483135b79fde28b12a10462617170001558cb5bed68ae85122` 

## Methodology

After navigating to the http://TARGET_IP:TARGET_PORT, we are greeted with a simple web page that has a text input field and a submit button.

![Homepage](screenshots/homepage.png)

It is clear that we are going to be working with a web application that is looking for us to input a string and check if it is the "Magical Palindrome" to release the flag.

I begin the Source Code Analysis and notice that there is a file called `\web_magical_palindrome\app\index.mjs` that contains the logic for the web application. The method `IsPalinDrome()` checks if a string is a palindrome and returns a string based on the result. So our solution is to create a string that is a palindrome and has a length of 1000 characters.

```javascript
// .... SNIPPET ....
const IsPalinDrome = (string) => {
	if (string.length < 1000) {
		return 'Tootus Shortus';
	}

	for (const i of Array(string.length).keys()) {
		const original = string[i];
		const reverse = string[string.length - i - 1];

		if (original !== reverse || typeof original !== 'string') {
			return 'Notter Palindromer!!';
		}
	}

	return null;
}
// .... SNIPPET ....
```

The following script generates a random palindrone that should be able to solve the box.

```python
import random
import string
random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=500))
palindrone = random_string + random_string[::-1]
print(palindrone)
```

However when we attempt to solve this problem using the generated palindrone, we get the following error:

![Error](screenshots/error.png)

Looking at the actual request we see that we are returned a `413 Request Entity Too Large` error. The request is being dropped by the nginx server, before it even reaches the application. We confirm this by looking at the NGINX configuration file. 

The NGINX configuration file shows that the `client_max_body_size` is set to `75` bytes. This is why we are getting the `413 Request Entity Too Large` error. However we need to 

Since the limit is `75 bytes`, the JSON array method is **impossible** because the array structure itself consumes too many characters/bytes.

You must find a way to send an array that the application interprets as having a `length of ≥1000`, but whose `total serialized JSON size is ≤75 bytes`.

The only way to represent a length of 1000 with very few characters is by exploiting some other type of vulnerability or language quirk.

I look for vulnerabilities in the importted packages `Hono` and `Fastify`, and can't find any. The versions of nginx and node.js are also up to date. 

After a lot of google searches and trying different things, I finally found a solution that revolves around manipulating the Implicit Type Conversion rules of JavaScript and the way the `Array()` constructor works on line 13 of `index.mjs`.

```javascript
// .... SNIPPET ....
if (string.length < 1000) {
// .... SNIPPET ....
for (const i of Array(string.length).keys()) {
// .... SNIPPET ....
```

According to the Ecma Standard (https://t   c39.es/ecma262/multipage/indexed-collections.html#sec-array-constructor), the `Array()` constructor behaves differently based on its arguments. If the first argument is a number, it creates an array with that number of elements. If the first argument is a string, it creates an array with the characters of the string. 
   
1. Single numeric argument: Creates an empty array with that length

    ```javascript
    Array(3)  // Creates: [empty × 3] with length 3
    ```

2. Single non-numeric argument: Creates an array containing that single element

    ```javascript
    Array("1000")  // Creates: ["1000"] with length 1
    ```

3. Multiple arguments: Creates an array with those elements

    ```javascript
    Array(1, 2, 3)  // Creates: [1, 2, 3]
    ```

So we exploit this quirk by passing in the following payload:

```json
{
    "palindrome": {
        "length": "1000",
        "0": "x",
        "999": "x"
    }
}
```

This passes the initial check because when  it goes to compare `if (string.length < 1000)` the `length` property of the object is implicitly converted to a number and compared to `1000`. Then when it goes to loop over the array `for (const i of Array(string.length).keys())`, since `"1000"` is a string, the `Array()` constructor creates an array with a length of 1, containing the string `"1000"`. Since the array has length 1, this loop only runs once with i = 0. 

The final check was the most difficult to configure as you had to know that `"1000" - 0 - 1` in JavaScript is implicitly converted to a number and performs arithmetic, which coerces the string to a number

```javascript
const original = string[0];                     // "x"
const reverse = string[string.length - 0 - 1];  // string["1000" - 0 - 1]
```

After crafting the exploit, we find that the payload size is only 50 bytes! Well under the 75-byte limit.

## Answer  

### Flag

```
HTB{Lum0s_M@x!ma}
```
