#!/bin/bash

TARGET_IP="83.136.251.105"
TARGET_PORT="40282"

# Use POST method to send the multi-line body
cat << EOF | curl http://$TARGET_IP:$TARGET_PORT/ -H "Content-Type: text/plain" --http0.9 -vvv --trace --data-raw @-
H:0
CX:0,1
H:1
CX:1,2
H:2
GET / HTTP/1.1
Host: $TARGET_IP:$TARGET_PORT
Content-Length: 0

EOF