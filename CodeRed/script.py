#!/bin/env python3
from PIL import Image
from pathlib import Path

def xor_strings(s, t):
        return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(s, t))

def xor_string_idx(s, i):
        return "".join(chr(ord(a) ^ i) for a in s)

def extract_pixels(imgPath_orig, imgPath_decode):
    image1 = Image.open(imgPath_orig)
    image2 = Image.open(imgPath_decode)
    red_band1 = image1.split()[0]
    red_band2 = image2.split()[0]
    xSize = image1.size[0];
    cipher1 = ""
    cipher2 = ""
    for i in range(0,xSize):
        if chr(red_band1.getpixel((i, 0))) != chr(red_band2.getpixel((i, 0))):
            cipher1 += chr(red_band1.getpixel((i, 0)))
            cipher2 += chr(red_band2.getpixel((i, 0)))
    return cipher1, cipher2

def decode_msg(a, b, i):
    c = xor_strings(a,b)
    d = xor_string_idx(c, i)
    return d

if __name__ == "__main__":
    a, b = extract_pixels("packet2.png", "57cf4c_0bf3bbad5f74409bad0a3a10b1dbd537~mv2.png");
    print(decode_msg(a, b, 0))
    a, b = extract_pixels("packet3.png", "57cf4c_0aa6e7ffcc024f7ba2b6611f72f2432d~mv2.png");
    print(decode_msg(a, b, 1))
    a, b = extract_pixels("packet4.png", "57cf4c_56a9ed0fd9c84c98935307aebb4783f7~mv2.png");
    print(decode_msg(a, b, 2))
    a, b = extract_pixels("packet5.png", "57cf4c_d9f88c5ddc93488d91ac03c56cc901ae~mv2.png");
    print(decode_msg(a, b, 3))
    a, b = extract_pixels("packet6.png", "57cf4c_4080f95bf84349e5887042c3a06f7114~mv2.png");
    print(decode_msg(a, b, 4))
    a, b = extract_pixels("packet7.png", "57cf4c_0bf3bbad5f74409bad0a3a10b1dbd537~mv2.png");
    print(decode_msg(a, b, 5))
    a, b = extract_pixels("packet8.png", "57cf4c_afea1f0bb82348d9bdc24653ea3208f9~mv2.png");
    print(decode_msg(a, b, 6))
    a, b = extract_pixels("packet9.png", "57cf4c_56a9ed0fd9c84c98935307aebb4783f7~mv2.png");
    print(decode_msg(a, b, 7))
    a, b = extract_pixels("packet10.png", "57cf4c_0aa6e7ffcc024f7ba2b6611f72f2432d~mv2.png");
    print(decode_msg(a, b, 8))

