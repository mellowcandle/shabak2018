#!/bin/env python3
from PIL import Image, ImageFont
from pathlib import Path

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

#        value_altered = ''.join(chr((ord(letter)+i) % 127)  for letter in a)

def print_inc(a, i):
    value_altered = ''.join(chr((ord(letter)+i) % 127)  for letter in a)
    return value_altered

    # str_list = list(value_altered)
    # for b in range(i - 1, len(str_list), i):
    #     print(b)
    #     str_list[b] = chr(ord(str_list[b]) - 2 )
    # print("".join(str_list))

def try_strings(a,b,i):
        print(print_inc(xor_strings(a,b),7))
    # for z in range (0,127):
    #     print(print_inc(xor_strings(a,b),z))
    


if __name__ == "__main__":
# execute only if run as a script
    # #dump_bytes("3decode.png")
    # a, b = extract_pixels("1.png", "1decode.png", 241, 260)
    # try_strings(a, b, 0)
    # a, b = extract_pixels("2.png", "s1.png", 241, 264) 
    
    # #Ajnap"jadidi."I'm"hipe0
    # #Ahlan habibi. I'm fine., How are you, 

    # try_strings(a, b, 1)
    # print("----")
    # a,b = extract_pixels("3.png", "s2.png", 241, 253)
    # try_strings(a, b,2)
    
    # print("---")
    # a,b = extract_pixels("2.png", "2decode.png", 241, 263)
    # try_strings(a, b, -1)
    # try_strings(a, b, 3)
    # print("---")
    #a,b = extract_pixels("5.png", "s3.png", 295, 335)
    #try_strings(a, b, 4)
    #try_strings(a, b, 4 - 14)

    # print("---")
    #a,b = extract_pixels("3.png", "3decode.png", 241, 253)
    #try_strings(a, b, 5)
    # print("---")
     #a,b = extract_pixels("4.png", "4decode.png", 241, 283)
     #try_strings(a, b, 6)
    # print("---")
     a,b = extract_pixels("3.png", "s4.png", 241, 288) # Got damn
     try_strings(a, b, 7)
    # print("---")
    
    #a,b = extract_pixels("5.png", "5decode.png", 295, 335)
    #try_strings(a, b, 8)
    # print("---")

   
