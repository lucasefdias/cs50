# HarvardX CS50: Introduction to Computer Science (edX 2018)
These are all my solutions to Harvard CS50's Problem Sets for the edX 2018 edition.<br/>
[Link to CS50 on edX](https://courses.edx.org/courses/course-v1:HarvardX+CS50+X/course/)<br/>
[Course's Syllabus](https://docs.cs50.net/2018/x/syllabus.html)<br/><br/>
**Disclaimer : The material in this repository is intended as portfolio to showcase the projects I have built during the course. I do not claim to have everything 100% error free. Please use caution when using the ideas here for production code. I will keep updating this code as I find bugs and/or find any improvements.**<br/><br/>

## Problem Set 0
Build a program in Scratch to start getting familiar with basic programming concepts.<br/>
[Instructions for PSET0](https://docs.cs50.net/2018/x/psets/0/pset0.html)<br/>
[Link to my PSET0](https://scratch.mit.edu/projects/204305134/)<br/>

## Problem Set 1: C
[Instructions for PSET1](https://docs.cs50.net/2018/x/psets/1/pset1.html)<br/>
### Hello
Implement a program that prints out a simple greeting to the user, per the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/1/hello/hello.html)
```
$ ./hello
hello, world
```

### Mario (less comfortable)
Implement a program that prints out a half-pyramid of a specified height, per the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/1/mario/less/mario.html)
```
$ ./mario
Height: 5
    ##
   ###
  ####
 #####
######

$ ./mario
Height: 3
  ##
 ###
####
```

### Mario (more comfortable)
Implement a program that prints out a double half-pyramid of a specified height, per the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/1/mario/more/mario.html)
```
$ ./mario
Height: 4
   #  #
  ##  ##
 ###  ###
####  ####
```

### Cash
Implement a program that calculates the minimum number of coins required to give a user change.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/1/cash/cash.html)
```
$ ./cash
Change owed: 0.41
4
```

### Credit
Implement a program that determines whether a provided credit card number is valid according to Luhn’s algorithm.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/1/credit/credit.html)
```
$ ./credit
Number: 378282246310005
AMEX
```

## Problem Set 2: Crypto
[Instructions for PSET2](https://docs.cs50.net/2018/x/psets/2/pset2.html)<br/>
### Caesar
Implement a program that encrypts messages using Caesar’s cipher, per the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/2/caesar/caesar.html)
```
$ ./caesar 13
plaintext:  HELLO
ciphertext: URYYB
```

### Vigenère
Implement a program that encrypts messages using Vigenère’s cipher, per the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/2/vigenere/vigenere.html)
```
$ ./vigenere ABC
plaintext:  HELLO
ciphertext: HFNLP
```

### Crack
Implement a program that cracks passwords, per the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/2/crack/crack.html)
```
$ ./crack 50fkUxYHbnXGw
rofl
```

## Problem Set 3: Music
Write a program that converts a sequence of notes read fom a text file into frequencies and synthesize the resulting song.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/3/music/music.html)

## Problem Set 4: Forensics
[Instructions for PSET4](https://docs.cs50.net/2018/x/psets/4/pset4.html)
### Whodunit
Answer some questions and then implement a program that reveals a hidden message in a BMP, per the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/4/whodunit/whodunit.html)
```
$ ./whodunit clue.bmp verdict.bmp
```

### Resize (less comfortable)
Implement a program that resizes BMPs, per the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/4/resize/less/resize.html)
```
$ ./resize 4 small.bmp large.bmp
```


### Resize (more comfortable)
Implement a program that resizes BMPs, per the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/4/resize/more/resize.html)
```
$ ./resize .25 large.bmp small.bmp
$ ./resize 4 small.bmp large.bmp
```

### Recover
Implement a program that recovers JPEGs from a forensic image, per the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/4/recover/recover.html)
```
$ ./recover card.raw
```

## Problem Set 5: Speller
Implement a program that spell-checks a file, per the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/5/speller/speller.html)
```
$ ./speller texts/lalaland.txt
MISSPELLED WORDS

[...]
AHHHHHHHHHHHHHHHHHHHHHHHHHHHT
[...]
Shangri
[...]
fianc
[...]
Sebastian's
[...]

WORDS MISSPELLED:
WORDS IN DICTIONARY:
WORDS IN TEXT:
TIME IN load:
TIME IN check:
TIME IN size:
TIME IN unload:
TIME IN TOTAL:
```

## Problem Set 6: Déjà vu
[Instructions for PSET6](https://docs.cs50.net/2018/x/psets/6/pset6.html)<br/>
### Sentimental
Port the programs in C from PSETs 1 and 2 to Python.<br/>
1. Port `hello.c` to `hello.py`.
1. Port `mario.c` to `mario.py`.
1. Port `cash.c` to `cash.py` or `credit.c` to `credit.py`.
1. Port `caesar.c` to `caesar.py`, `vigenere.c` to `vigenere.py`, or `crack.c` to `crack.py`.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/6/sentimental/sentimental)

### Similarities (less confortable)
1.Implement a program that compares two files for similarities.
1.Implement a website that highlights similarities across files, a la the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/6/similarities/less/similarities.html)<br/>
![Similarities (less) output](./similarities-less.png?raw=true)

### Similarities (more confortable)
1.Implement a program that measures the edit distance between two strings.
1.Implement a web app that depicts the costs of transforming one string into another, a la the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/6/similarities/more/similarities.html)<br/>
![Similarities (more) output](./similarities-more.png?raw=true)

## Problem Set 7: C$50 Finance
Implement a website via which users can "buy" and "sell" stocks, a la the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/7/finance/finance.html)<br/>
![C$50 Finance output](./cs50finance.png?raw=true)

## Problem Set 8: Mashup
Implement a website that lets users search for articles atop a map, a la the below.<br/>
[Full specification](https://docs.cs50.net/2018/x/psets/8/mashup/mashup.html)<br/>
![Mashup output](./mashup.png?raw=true)
