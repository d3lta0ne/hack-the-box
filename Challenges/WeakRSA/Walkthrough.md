# Challenge Description
Can you decrypt the message and get the flag?

Zip Password: `hackthebox`
SHA-256: `1cbf890e7a0fe8b404597b565da96c388e5653937631e2dc8710ede9d15bdb7d`
# Solution

We find the needed python module called [RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool) to solve this challenge.

```bash
git clone https://github.com/RsaCtfTool/RsaCtfTool
```

After cloning the git repo we run the following command to get the flag. We will use pipenv to maintain interoperatability with the systems.

```bash
pipenv install -r RsaCtfTool/requirements.txt 
```

After ensuring that our virtual enviornment is properly setup we run the following command to get our flag.

```bash
pipenv run python RsaCtfTool/RsaCtfTool.py --publickey key.pub --decryptfile flag.enc
```

## Flag
`HTB{s1mpl3_Wi3n3rs_4tt4ck`
