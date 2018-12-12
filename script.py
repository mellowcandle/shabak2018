#!/bin/env python3
from PIL import Image, ImageFont
import textwrap
from pathlib import Path
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyz'

def xor_strings(s, t):
    """xor two strings together"""
    if isinstance(s, str):
        return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(s, t))
    else:
        return bytes([a ^ b for a, b in zip(s, t)])

def or_strings(s, t):
    """xor two strings together"""
    if isinstance(s, str):
        return "".join(chr(ord(a) | ord(b)) for a, b in zip(s, t))
    else:
        return bytes([a | b for a, b in zip(s, t)])

def del_strings(s, t):
    """xor two strings together"""
    if isinstance(s, str):
        return "".join(chr(ord(a) - ord(b) if ord(a) > ord(b) else ord(b) - ord(a)) for a, b in zip(s, t))
    else:
        return bytes([a & b for a, b in zip(s, t)])


def and_strings(s, t):
    """xor two strings together"""
    if isinstance(s, str):
        return "".join(chr(ord(a) & ord(b)) for a, b in zip(s, t))
    else:
        return bytes([a & b for a, b in zip(s, t)])

def add_strings(s, t):
    """xor two strings together"""
    if isinstance(s, str):
        return "".join(chr(ord(a) + ord(b)) for a, b in zip(s, t))
    else:
        return bytes([a & b for a, b in zip(s, t)])

def Rotate(key: int) -> str:
    rotate = ""
    for l in alphabet:
        if l in alphabet:
             rotate += alphabet[(alphabet.index(l) + key) % (len(alphabet))]
    return rotate

def extract_pixels(imgPath_orig, imgPath_decode, start, end):
    image1 = Image.open(imgPath_orig)
    image2 = Image.open(imgPath_decode)
    red_band1 = image1.split()[0]
    red_band2 = image2.split()[0]
    cipher1 = ""
    cipher2 = ""
    for i in range(start,end):
        cipher1 += chr(red_band1.getpixel((i, 0)))
        cipher2 += chr(red_band2.getpixel((i, 0)))
    return cipher1, cipher2



#   xor_string = xor_strings(cipher1, cipher2)
#    print(xor_string)
#    for key in range(44):
#        Rotate(key)
#        table = str.maketrans(Rotate(key), alphabet)
#        print(xor_string.translate(table))
#
#    print("")
#    for i in range(start,end):
#        if red_band1.getpixel((i, 0)) != red_band2.getpixel((i, 0)):
#                print(chr(red_band1.getpixel((i, 0)) | red_band2.getpixel((i, 0))), end='')
#    print("")
#    for i in range(start,end):
#        if red_band1.getpixel((i, 0)) != red_band2.getpixel((i, 0)):
#                print(chr(red_band1.getpixel((i, 0)) & red_band2.getpixel((i, 0))), end='')
#    print("")
#
#    for i in range(start,end):
#        if red_band1.getpixel((i, 0)) != red_band2.getpixel((i, 0)):
#                print(chr(red_band1.getpixel((i, 0)) + red_band2.getpixel((i, 0))), end='')
#
#    print("")
#    for i in range(start,end):
#        if red_band1.getpixel((i, 0)) != red_band2.getpixel((i, 0)):
#                print(chr(red_band2.getpixel((i, 0))), end='')
    print("")

def try_strings(a,b):
    print("Attemting to crack")
    print(xor_strings(a,b))
    print(or_strings(a,b))
    print(and_strings(a,b))
    print(del_strings(a,b))
    print(add_strings(a,b))
    print(b)

def dump_bytes(a):
    image = Image.open(a)
    red_band = image.split()[0]
    for i in range(0,400):
        for j in range(0,400):
            if red_band.getpixel((i, j)) == 72:
                if red_band.getpixel((i+1, j)) == 20:
                    print(i,j)



if __name__ == "__main__":
# execute only if run as a script
    dump_bytes("3decode.png")
    a, b = extract_pixels("1.png", "1decode.png", 241, 260)
    try_strings(a, b)
    a, b = extract_pixels("2.png", "s1.png", 241, 264)
    try_strings(a, b)

    a,b = extract_pixels("3.png", "s2.png", 241, 253)
    try_strings(a, b)
    a,b = extract_pixels("2.png", "2decode.png", 241, 263)
    try_strings(a, b)
    a,b = extract_pixels("5.png", "s3.png", 295, 335)
    try_strings(a, b)
    a,b = extract_pixels("3.png", "3decode.png", 241, 253)
    try_strings(a, b)
    a,b = extract_pixels("4.png", "4decode.png", 241, 283)
    try_strings(a, b)
    a,b = extract_pixels("3.png", "s4.png", 241, 288)
    try_strings(a, b)
    a,b = extract_pixels("5.png", "5decode.png", 295, 335)
    try_strings(a, b)

15 
   # extract_pixels("1decode.png", "2decode.png", 241, 263)
   # print("New line")
   # extract_pixels("3.png", "3decode.png", 241, 253)
   # print("New line")
   # extract_pixels("4.png", "4decode.png", 241, 283)
   # print("New line")
   # extract_pixels("5.png", "5decode.png", 295, 335)
   # print("New line")
   # extract_pixels("2.png", "s1.png", 241, 264)
   # print("New line")
  # print("New line")
   # extract_pixels("3.png", "s4.png", 241, 288)
   # print("New line")

#    find_text_in_image("3decode.png")
#    find_text_in_image("decoded_20181210143035.png")
