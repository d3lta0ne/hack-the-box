#!/bin/bash
docker rm -f web_breahtaking_view
docker build --no-cache --tag=web_breahtaking_view .
docker run -p 1337:8081 --rm --name=web_breahtaking_view -it web_breahtaking_view