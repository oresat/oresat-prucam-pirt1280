#!/usr/bin/python3

import io
import os

import cv2
import numpy as np

cols = 1280
rows = 1024
pixel_bytes = cols * rows * 2

path = "/dev/prucam"
gpio_num = 86

# enable sensor
with open(f"/sys/class/gpio/gpio{gpio_num}/value", "w") as f:
    f.write("1")

# open up the prucam char device
fd = os.open(path, os.O_RDWR)
fio = io.FileIO(fd, closefd=False)

# make buffer to read into
imgbuf = bytearray(pixel_bytes)

# read from prucam into buffer
fio.readinto(imgbuf)

# write raw buffer out to file
out = open("img.buf", "wb")
out.write(imgbuf)

# read image bytes into ndarray
img = np.frombuffer(imgbuf, dtype=np.uint16).reshape(rows, cols)

# flip the image vertically because it is read upside down
img = cv2.flip(img, 0)

# json encode image
ok, img = cv2.imencode(".png", img, params=[cv2.CV_16U])
if not (ok):
    raise BaseException("encoding error")

# write image
with open("img.png", "wb") as f:
    f.write(img)
