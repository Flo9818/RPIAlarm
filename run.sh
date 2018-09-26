#!/bin/sh

NAME=rpi-alarm
docker kill ${NAME}
docker rm ${NAME}
docker run -d \
    -p 5000:5000 \
    -p 3000:3000 \
    --name ${NAME}  \
    rpi-alarm