# Week2 CTF Solutions

## Classic Caesar

The name of the challenge hints at caesar cipher being used to encode the flag. Using cyberchef we find the decoded flag.

![caesar.png](caesar.png?raw=true "caesar.png")

> Flag: dcCTF{CAESAR_NEVER_DIES}

## Oui Oui Secret

The secret in the challenge name hints at Vignere Cipher. Bruteforcing the key gives away the flag.

![vignere.png](vignere.png?raw=true "vignere.png")

> Flag: dcCTF{how_did_you_bruteforce_this}

## Fair Enough

Again, the name of the challenge and cipher-identifier hint at Playfair cipher being used. Bruteforcing the cipher gives the flag.

![playfair.png](playfair.png?raw=true "playfair.png")

> Flag: dcCTF{BUTAREYOUPLAYINGFAIR}

## Weak RSA

The text file contains n, e and c. If we want to decode the ciphertext we need to find d, for which we would require both p and q. We try to factorize n and we do find p and q respectively.

```zsh
┌──(kali㉿kali)-[~/Downloads]
└─$ cat rsa.txt 
n = 57778696010931478770084557840702815787537804896513745039042529220741201603183
e = 65537
c = 19759948204827148967716452284363638954256347121332992994807595069379938069646
                                                                                     
┌──(kali㉿kali)-[~/Downloads]
└─$ 
```

![factorize.png](factorize.png?raw=true "factorize.png")

We can now use p and q to calculate d. Then using d and n we can decrypt the ciphertext and obtain the flag.

```zsh
┌──(kali㉿kali)-[~/Downloads]
└─$ python3    
Python 3.13.3 (main, Apr 10 2025, 21:38:51) [GCC 14.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> p = 219920443573698782845930677192261022747 
>>> q = 262725443219511029142449525203053232189
>>> e = 65537
>>> n = 5777869601093147877008455784070281578753780489651374503904252922074120160318\
3
>>> c = 1975994820482714896771645228436363895425634712133299299480759506937993806964\
6
>>> phi = (p-1)*(q-1)
>>> d = mod(e, -1, phi)
Traceback (most recent call last):
  File "<python-input-6>", line 1, in <module>
    d = mod(e, -1, phi)
        ^^^
NameError: name 'mod' is not defined
>>> d = pow(e, -1, phi)
>>> m = pow(c, d, n)
>>> m.to_bytes((m.bit_length() + 7) // 8, 'big').decode('ascii')
'dcCTF{W34k_RSA_1s_N0_G00D}'
>>> 
```

> Flag: dcCTF{W34k_RSA_1s_N0_G00D}

## XOR

The flag is XORed with a key and then hex encoded. Since we know that the flag will always start with `dcCTF{`, we can use the known plaintext attack. Using cyberchef we find the repeating key as `sand`.

![xor1.png](xor1.png?raw=true "xor1.png")

And using that as the key, we obtain the flag.

![xor2.png](xor2.png?raw=true "xor2.png")

> Flag: dcCTF{d0nT_R3peAt_x0R}

## Hidden in Plain Sight

We are given a jpeg file with some sort of embedded flag. Running stegseek gives it away.

```zsh
┌──(bruh)─(kali㉿kali)-[~/Downloads]
└─$ file miku.jpg                                             
miku.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 708x1200, components 3
                                                                                     
┌──(bruh)─(kali㉿kali)-[~/Downloads]
└─$ stegseek -sf miku.jpg          
StegSeek 0.6 - https://github.com/RickdeJager/StegSeek

[i] Found passphrase: "hatsune"        
[i] Original filename: "flag.txt".
[i] Extracting to "miku.jpg.out".

                                                                                     
┌──(bruh)─(kali㉿kali)-[~/Downloads]
└─$ cat miku.jpg.out   
dcCTF{h1d1ng_1n_y0ur_w1f1}
                                                                                
┌──(bruh)─(kali㉿kali)-[~/Downloads]
└─$ 
```

> Flag: dcCTF{h1d1ng_1n_y0ur_w1f1}

## Chameleon Image

We find another jpeg file. Running binwalk reveals it to be a polyglot zip file which contains the flag.

```zsh
┌──(bruh)─(kali㉿kali)-[~/Downloads]
└─$ file mystery_file.jpg 
mystery_file.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 400x300, components 3
                                                                                     
┌──(bruh)─(kali㉿kali)-[~/Downloads]
└─$ binwalk -e mystery_file.jpg 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
6563          0x19A3          Zip archive data, at least v2.0 to extract, compressed size: 32, uncompressed size: 32, name: flag.txt
6633          0x19E9          Zip archive data, at least v2.0 to extract, compressed size: 32, uncompressed size: 32, name: readme.txt
6705          0x1A31          Zip archive data, at least v2.0 to extract, compressed size: 29, uncompressed size: 29, name: secret.txt
6774          0x1A76          Zip archive data, at least v2.0 to extract, compressed size: 28, uncompressed size: 28, name: hidden/treasure.txt

WARNING: One or more files failed to extract: either no utility was found or it's unimplemented

                                                                                     
┌──(bruh)─(kali㉿kali)-[~/Downloads]
└─$ cat _mystery_file.jpg.extracted/flag.txt 
dcCTF{POLYGLOT_FILES_ARE_SNEAKY}

┌──(bruh)─(kali㉿kali)-[~/Downloads]
└─$ 
```

> Flag: dcCTF{POLYGLOT_FILES_ARE_SNEAKY}

## Sound of Secrets

This time we are given a .wav file. Listening to it results in some sort of beep sounds, which hint at it being morse code. Decoding the morse code gives the flag.

![morse1.png](morse1.png?raw=true "morse1.png")

![morse2.png](morse2.png?raw=true "morse2.png")

> Flag: dcCTF{r34lfl4g}

## Cropped Antics

We are given a single-paged pdf file which has a cropped image. We use pdfimages to get the full uncropped image and obtain the flag.

![cropped.png](cropped.png?raw=true "cropped.png")

> Flag: dcCTF{Cr0p3d_pDF}

## Evidence Disk

We are given ext2 filesystem linux disk image. Running foremost gives us a bunch of decoy png files along with the flag file.

![foremost.png](foremost.png?raw=true "foremost.png")

> Flag: dcCTF{FILE_RECOVERY_SUCCESS}

## Network Intrusion

We are given a pcap file for analysis. Opening it up in wireshark, it contains a bunch of HTTP and malformed DNS packets. Looking through one of the DNS packets, we find this domain.

![wireshark.png](wireshark.png?raw=true "wireshark.png")

Decoding the subdomain part of the domain, we obtain the flag.

```zsh
┌──(kali㉿kali)-[~]
└─$ echo ZGNDVEZ7TDBDNExIMFNUX0RONV8zWEYxTFRSNFQxME59 | base64 -d
dcCTF{L0C4LH0ST_DN5_3XF1LTR4T10N}      

┌──(kali㉿kali)-[~]
└─$ 
```

> Flag: dcCTF{L0C4LH0ST_DN5_3XF1LTR4T10N}

## Lots of Notes

We are given another jpeg file. Running stegseek results in a mp3 file. Listening to that mp3 file, it contains weird beeping signals.

```zsh
└─$ file notes.jpg                                            
notes.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 2000x2000, segment length 16, baseline, precision 8, 12729x7937, components 3
                                                                                     
┌──(kali㉿kali)-[~]
└─$ stegseek -sf notes.jpg         
StegSeek 0.6 - https://github.com/RickdeJager/StegSeek
[i] Found passphrase: ""
[i] Original filename: "20250609_231659.mp3".
[i] Extracting to "notes.jpg.out".

┌──(kali㉿kali)-[~]
└─$                       
```

Based on the challenge text, "sending content over radio" hints at SSTV signals. We use RX-SSTV for decryption, along with VLC Media Player and a virtual audio cable driver. Running them together decodes the flag.

![sstv.png](sstv.png?raw=true "sstv.png")

> Flag: dcCTF{B33P_B00P}
