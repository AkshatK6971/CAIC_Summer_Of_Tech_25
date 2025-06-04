# Week1 CTF Solutions

## Welcome Agent

SSHing with the credentials provided of ctfuser:ctfpassword on port 2201 of 3.7.66.170, the flag is present in our home directory.

```zsh
ctfuser@1443730f6336:~$ ls -la
total 24
dr-xr-xr-x 1 ctfuser ctfuser 4096 Jun  2 12:26 .
drwxr-xr-x 1 root    root    4096 Jun  2 12:26 ..
-rw-r--r-- 1 ctfuser ctfuser  220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 ctfuser ctfuser 3771 Feb 25  2020 .bashrc
-rw-r--r-- 1 ctfuser ctfuser  807 Feb 25  2020 .profile
-r--r--r-- 1 root    root      29 Jun  2 12:26 flag.txt
ctfuser@1443730f6336:~$ cat flag.txt 
dcCTF{w3lc0me_t0_7h3_m4tr1x}
ctfuser@1443730f6336:~$ 
```

> Flag: dcCTF{w3lc0me_t0_7h3_m4tr1x}

## Hidden in the Crowd

Again, SSHing with the credentials provided of ctfuser:ctfpassword on port 2210, we are greeted with a bunch of random files with decoy flags.

```zsh
ctfuser@27ef61cae115:~$ ls
00D3G  53Xo4  Awh2S  GDom9  LYRDl  R84Bf  W68Sh  ayxO7  gRqMP  lQSxk  qn77g  vVi3X
03pdH  547cR  Axd1c  GPdXf  LZe9t  R9Eps  W6C0b  b6SSS  gUHYk  lRU1y  qqZ2H  vcfQ4
04opP  5Fdu8  AzTmK  GXylx  Lb35B  RDVdL  WAfW3  b76P9  gWvXl  lU8DO  qsugk  vgaYe

<snip>....</snip>

ctfuser@27ef61cae115:~$ ls | wc -l
1000
ctfuser@27ef61cae115:~$ cat 00D3G 
incorrect{d3c0y_fl4g_00D3G}
ctfuser@27ef61cae115:~$ 
```

Ignoring the decoy flags, we find the flag as a hidden file in the directory.

```zsh
ctfuser@27ef61cae115:~$ ls -la | head
total 4048
dr-xr-xr-x 1 ctfuser ctfuser 28672 Jun  2 12:29 .
drwxr-xr-x 1 root    root     4096 Jun  2 12:26 ..
-rw-r--r-- 1 ctfuser ctfuser   220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 ctfuser ctfuser  3771 Feb 25  2020 .bashrc
-r--r--r-- 1 root    root       38 Jun  2 12:29 .flag
-rw-r--r-- 1 ctfuser ctfuser   807 Feb 25  2020 .profile
-r--r--r-- 1 root    root       28 Jun  2 12:29 00D3G
-r--r--r-- 1 root    root       28 Jun  2 12:29 03pdH
-r--r--r-- 1 root    root       28 Jun  2 12:29 04opP
ctfuser@27ef61cae115:~$ cat .flag 
dcCTF{h1dd3n_f1l3s_4r3_n07_s0_h1dd3n}
ctfuser@27ef61cae115:~$ 
```

> Flag:  dcCTF{h1dd3n_f1l3s_4r3_n07_s0_h1dd3n}

## Log explore

Downloading the loggen file results in a log.txt file which is too large to read at once and hangs out.

```zsh
┌──(kali㉿kali)-[~/Downloads]
└─$ file logGen 
logGen: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=7c664b7d6577b794f1be704376544d6178a2a6ee, for GNU/Linux 3.2.0, not stripped
                                                                                     
┌──(kali㉿kali)-[~/Downloads]
└─$ ./logGen 
Log file generated.
                                                                                     
┌──(kali㉿kali)-[~/Downloads]
└─$ ls -l log.txt 
-rw-r--r-- 1 kali kali 17179869184 Jun  3 20:25 log.txt
                                                                                     
┌──(kali㉿kali)-[~/Downloads]
└─$ head log.txt
Log checkpoint at offset 0 MB: All systems OK.


```

Running strings on the binary does indeed show the function responsible for printing that flag. Running ltrace and looking through the output gives it away.

```zsh
┌──(kali㉿kali)-[~/Downloads]
└─$ strings logGen| grep flag
!! ALERT: hidden flag --> 
!! ALERT: hiddenhidden flag --> 000102030405060708091011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980818283848586878889909192939495293949596979899
_ZL14encrypted_flag
_Z12decrypt_flagB5cxx11v.cold
_Z12decrypt_flagB5cxx11v
                                                                                     
┌──(kali㉿kali)-[~/Downloads]
└─$ ltrace ./logGen       
open("log.txt", 0x241, 0644)                        = 3
lseek(3, 0, SEEK_SET)                               = 0
_Znwm(31)                                           = 0x555dcad582b0
_Znwm(61)                                           = 0x555dcad582e0
memcpy(0x555dcad582e0, "Log checkpoint at offset 0", 26) = 0x555dcad582e0
memcpy(0x555dcad582fa, " MB: All systems OK.\n", 21) = 0x555dcad582fa

<snip>...</snip>

write(3, "Log checkpoint at offset 2000 MB"..., 50) = 50
_ZdlPvm(0x555dcad582e0, 61, 50, 0x7ffe3bc47b10)     = 1
lseek(3, 2621440000, SEEK_SET)                      = 2621440000
_Znwm(41)                                           = 0x555dcad58330
memcpy(0x555dcad5834a, "dcCTF{b1G_L0g}", 14)        = 0x555dcad5834a
_Znwm(81)                                           = 0x555dcad58370
memcpy(0x555dcad58370, "!! ALERT: hidden flag --> dcCTF{"..., 40) = 0x555dcad58370
_ZdlPvm(0x555dcad58330, 41, 40, 0x555dcad58370)     = 1
write(3, "!! ALERT: hidden flag --> dcCTF{"..., 41) = 41
_ZdlPvm(0x555dcad58370, 81, 41, 40)                 = 1

<snip>...</snip>
```

> Flag: dcCTF{b1G_L0g}

## Process Hunter

SSHing with the credentials of ctfuser:ctfpassword, we check the running processes and grab the flag.

```zsh
ctfuser@6af6cf517167:~$ ps -ef | grep CTF
root           1       0  0 11:16 ?        00:00:00 /bin/sh -c /usr/sbin/sshd && sleep --flag=dcCTF{ps_aux_r3v34l5_4ll} 99999999 & /usr/sbin/sshd -D
ctfuser       48      42  0 11:17 pts/0    00:00:00 grep --color=auto CTF
ctfuser@6af6cf517167:~$ 
```

> Flag: dcCTF{ps_aux_r3v34l5_4ll}

## LockedVault

Downloading the given .tar.gz file and opening it results in some bash files along with a Readme.

```zsh
┌──(kali㉿kali)-[~/Downloads]
└─$ tar -xvzf LockedVault.tar.gz
LockedVault/
LockedVault/step1.sh
LockedVault/step2.sh
LockedVault/step3.sh
LockedVault/README.txt
                                                                                     
┌──(kali㉿kali)-[~/Downloads]
└─$ cd LockedVault        
                                                                                     
┌──(kali㉿kali)-[~/Downloads/LockedVault]
└─$ cat README.txt        
LOCKED VAULT CHALLENGE

You have 3 scripts but they have restrictive permissions:
- step1.sh: Cannot be read (need to fix permissions to see the password)
- step2.sh: Cannot be executed (need to make executable and use password from step1)  
- step3.sh: Cannot be read (need to fix permissions and use key from step2)

Each script checks for the correct input from the previous step.
Even if you bypass permissions with sudo, you still need to solve each step properly!

Start by fixing permissions on step1.sh and reading it.
```

Simply give rwx(777) permissions to all the files and execute them to obtain the flag.

```zsh
┌──(kali㉿kali)-[~/Downloads/LockedVault]
└─$ chmod 777 *
                                                                                     
┌──(kali㉿kali)-[~/Downloads/LockedVault]
└─$ bash step1.sh                       
Step 1 complete!
Password found: unlock123
Now make step2.sh executable and run it with this password!
                                                                                     
┌──(kali㉿kali)-[~/Downloads/LockedVault]
└─$ bash step2.sh
Enter the password from step1:
unlock123
Correct! Moving to final step...
Key for step3: final_key_456
                                                                                     
┌──(kali㉿kali)-[~/Downloads/LockedVault]
└─$ bash step3.sh
Enter the key from step2:
final_key_456
Vault unlocked!
Flag: dcCTF{y0u_4r3_4_p3rm1ss10n_h0ckcr_n0w}
```

> Flag: dcCTF{y0u_4r3_4_p3rm1ss10n_h0ckcr_n0w}

## Dumpster Diver

The downloaded file is an ELF file which keeps on running forever. My initial attempts at using ltrace and strace did not help. Strings show us an encrypt_flag and a decrypt_flag function with mangled function names.

```zsh
┌──(kali㉿kali)-[~/Downloads]
└─$ ./program 
Running forever...

^C                                                                                    
┌──(kali㉿kali)-[~/Downloads]
└─$ strings program | grep flag
_ZL14encrypted_flag
_ZNSt9once_flagC2Ev
_ZNSt9once_flagC1Ev
_ZNSt13__future_base13_State_baseV221_M_set_retrieved_flagEv
_Z12decrypt_flagB5cxx11v
_ZNSt11atomic_flagC1Eb
_ZNSt11atomic_flagC2Eb
_ZNSt11atomic_flag7_S_initEb
                                                                                     
┌──(kali㉿kali)-[~/Downloads]
└─$ c++filt _Z12decrypt_flagB5cxx11v

decrypt_flag[abi:cxx11]()
┌──(kali㉿kali)-[~/Downloads]
└─$ 
```

Time to go for dynamic analysis I suppose. Stepping over the decrypt_flag function shows the flag inside the memory within the rax, rsp or rdi register.

```zsh
gef➤  b *decrypt_flag
Breakpoint 1 at 0x22b9
gef➤  r
Starting program: /home/kali/Downloads/program 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Running forever...

Breakpoint 1, 0x00005555555562b9 in decrypt_flag[abi:cxx11]() ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x00007fffffffdcd0  →  0x00000000000011ff
$rbx   : 0x00007fffffffde48  →  0x00007fffffffe1c2  →  "/home/kali/Downloads/program"
$rcx   : 0x0000555555559058  →  "Running forever...\n"
$rdx   : 0x00007ffff7e5c310  →  0x00007ffff7d3f6f0  →  <std::basic_ostream<char, std::char_traits<char> >::~basic_ostream()+0000> endbr64 
$rsp   : 0x00007fffffffdcc8  →  0x000055555555636b  →  <main+002e> lea rax, [rbp-0x30]
$rbp   : 0x00007fffffffdd30  →  0x0000000000000001
$rsi   : 0x000055555556f2b0  →  "Running forever...\n"
$rdi   : 0x00007fffffffdcd0  →  0x00000000000011ff
$rip   : 0x00005555555562b9  →  <decrypt_flag[abi:cxx11]()+0000> push rbp
$r8    : 0x0               
$r9    : 0x0               
$r10   : 0x0               
$r11   : 0x202             
$r12   : 0x0               
$r13   : 0x00007fffffffde58  →  0x00007fffffffe1df  →  "COLORFGBG=15;0"
$r14   : 0x00007ffff7ffd000  →  0x00007ffff7ffe310  →  0x0000555555554000  →   jg 0x555555554047
$r15   : 0x000055555555bc38  →  0x0000555555556270  →  <__do_global_dtors_aux+0000> endbr64 
$eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00 
────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdcc8│+0x0000: 0x000055555555636b  →  <main+002e> lea rax, [rbp-0x30]   ← $rsp                                                                               
0x00007fffffffdcd0│+0x0008: 0x00000000000011ff   ← $rax, $rdi
0x00007fffffffdcd8│+0x0010: 0xffffffffffffff98
0x00007fffffffdce0│+0x0018: 0x6c6f6f705f68652e
0x00007fffffffdce8│+0x0020: 0x00007ffff7bf1ac0  →  0x0000000000000000
0x00007fffffffdcf0│+0x0028: 0x00000000000011ff
0x00007fffffffdcf8│+0x0030: 0xffffffffffffff98
0x00007fffffffdd00│+0x0038: 0x6c6f6f705f68652e
──────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x5555555562a9 <__do_global_dtors_aux+0039> nop    DWORD PTR [rax+0x0]
   0x5555555562b0 <frame_dummy+0000> endbr64 
   0x5555555562b4 <frame_dummy+0004> jmp    0x555555556230 <register_tm_clones>
●→ 0x5555555562b9 <decrypt_flag[abi:cxx11]()+0000> push   rbp
   0x5555555562ba <decrypt_flag[abi:cxx11]()+0001> mov    rbp, rsp
   0x5555555562bd <decrypt_flag[abi:cxx11]()+0004> push   rbx
   0x5555555562be <decrypt_flag[abi:cxx11]()+0005> sub    rsp, 0x28
   0x5555555562c2 <decrypt_flag[abi:cxx11]()+0009> mov    QWORD PTR [rbp-0x28], rdi
   0x5555555562c6 <decrypt_flag[abi:cxx11]()+000d> mov    rax, QWORD PTR [rbp-0x28]
──────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "program", stopped 0x5555555562b9 in decrypt_flag[abi:cxx11]() (), reason: BREAKPOINT
────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x5555555562b9 → decrypt_flag[abi:cxx11]()()
[#1] 0x55555555636b → main()
─────────────────────────────────────────────────────────────────────────────────────
gef➤  step
Single stepping until exit from function _Z12decrypt_flagB5cxx11v,
which has no line number information.
0x000055555555636b in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x00007fffffffdcd0  →  0x000055555556f6c0  →  "dcCTF{m3m0ry_dump_fl4g}B"
$rbx   : 0x00007fffffffde48  →  0x00007fffffffe1c2  →  "/home/kali/Downloads/program"
$rcx   : 0x336d7b4654436364 ("dcCTF{m3"?)
$rdx   : 0x1e              
$rsp   : 0x00007fffffffdcd0  →  0x000055555556f6c0  →  "dcCTF{m3m0ry_dump_fl4g}B"
$rbp   : 0x00007fffffffdd30  →  0x0000000000000001
$rsi   : 0x42              
$rdi   : 0x00007fffffffdcd0  →  0x000055555556f6c0  →  "dcCTF{m3m0ry_dump_fl4g}B"
$rip   : 0x000055555555636b  →  <main+002e> lea rax, [rbp-0x30]
$r8    : 0x00007ffff7bf1ac0  →  0x0000000000000000
$r9    : 0x1               
$r10   : 0x6               
$r11   : 0x00007ffff7b89f40  →  <__memmove_ssse3+0000> mov rax, rdi
$r12   : 0x0               
$r13   : 0x00007fffffffde58  →  0x00007fffffffe1df  →  "COLORFGBG=15;0"
$r14   : 0x00007ffff7ffd000  →  0x00007ffff7ffe310  →  0x0000555555554000  →   jg 0x555555554047
$r15   : 0x000055555555bc38  →  0x0000555555556270  →  <__do_global_dtors_aux+0000> endbr64 
$eflags: [zero carry parity adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00 
────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdcd0│+0x0000: 0x000055555556f6c0  →  "dcCTF{m3m0ry_dump_fl4g}B"    ← $rax, $rsp, $rdi                                                                       
0x00007fffffffdcd8│+0x0008: 0x0000000000000018
0x00007fffffffdce0│+0x0010: 0x000000000000001e
0x00007fffffffdce8│+0x0018: 0x0075645f7972306d ("m0ry_du"?)
0x00007fffffffdcf0│+0x0020: 0x00000000000011ff
0x00007fffffffdcf8│+0x0028: 0xffffffffffffff98
0x00007fffffffdd00│+0x0030: 0x6c6f6f705f68652e
0x00007fffffffdd08│+0x0038: 0x00007ffff7e54398  →  0x00007ffff7cb0270  →   endbr64 
──────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x55555555635f <main+0022>      lea    rax, [rbp-0x60]
   0x555555556363 <main+0026>      mov    rdi, rax
   0x555555556366 <main+0029>      call   0x5555555562b9 <_Z12decrypt_flagB5cxx11v>
 → 0x55555555636b <main+002e>      lea    rax, [rbp-0x30]
   0x55555555636f <main+0032>      mov    rdi, rax
   0x555555556372 <main+0035>      call   0x555555556d52 <_ZNSt7promiseIvEC2Ev>
   0x555555556377 <main+003a>      lea    rax, [rbp-0x40]
   0x55555555637b <main+003e>      lea    rdx, [rbp-0x30]
   0x55555555637f <main+0042>      mov    rsi, rdx
──────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "program", stopped 0x55555555636b in main (), reason: SINGLE STEP
────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x55555555636b → main()
────────────────────────────────────────────
```

> Flag: dcCTF{m3m0ry_dump_fl4g}

## Git Gud

Downloading the file and unzipping it results in a git repo. Checking logs show a commit with message of adding a sensitive file, probably the flag.

```zsh
┌──(kali㉿kali)-[~/Downloads/git_forensics_challenge]
└─$ ls -la | head
total 28
drwxr-xr-x 3 kali kali  4096 Jun  2 20:22 .
drwxr-xr-x 3 kali kali 16384 Jun  4 17:02 ..
drwxr-xr-x 7 kali kali  4096 Jun  2 20:22 .git
-rw-r--r-- 1 kali kali    51 Jun  2 20:22 README.md
                                                                                     
┌──(kali㉿kali)-[~/Downloads/git_forensics_challenge]
└─$ git log                                          
commit 1020cf6b231c9c2702a62e745c119bc6f7938970 (HEAD -> master)
Author: Z3R0C1PH3R <Z3R0C1PH3R@protonmail.com>
Date:   Mon Jun 2 20:22:49 2025 +0530

    Update README again

commit 1e2d1d684ee24693070677e9620ea6afb4fa31df
Author: Z3R0C1PH3R <Z3R0C1PH3R@protonmail.com>
Date:   Mon Jun 2 20:22:49 2025 +0530

    Remove flag

commit 5750476ca64e3a900c8b97f7cbae2578c79955b8
Author: Z3R0C1PH3R <Z3R0C1PH3R@protonmail.com>
Date:   Mon Jun 2 20:22:49 2025 +0530

    Add sensitive file

commit 63497d90d523d389530e56d18e4b285e31ad6646
Author: Z3R0C1PH3R <Z3R0C1PH3R@protonmail.com>
Date:   Mon Jun 2 20:22:49 2025 +0530

    Initial commit
                                                                                     
┌──(kali㉿kali)-[~/Downloads/git_forensics_challenge]
└─$ 
```

Checking the difference between the 'Add sensitive file' commit and the current one, we find the flag.

```zsh
┌──(kali㉿kali)-[~/Downloads/git_forensics_challenge]
└─$ git diff 5750476ca64e3a900c8b97f7cbae2578c79955b8
diff --git a/README.md b/README.md
index 9297bd6..a2c69dc 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,2 @@
 This is a sample README.
+Just some boring changes.
diff --git a/flag.txt b/flag.txt
deleted file mode 100644
index e58e971..0000000
--- a/flag.txt
+++ /dev/null
@@ -1 +0,0 @@
-dcCTF{g17_0bj3ct5_n3v3r_d13}
                                                                                     
┌──(kali㉿kali)-[~/Downloads/git_forensics_challenge]
└─$ 
```

> Flag: dcCTF{g17_0bj3ct5_n3v3r_d13}

## Event Digger

The following string is provided to us which looks like a base64 encoded string. Decoding it results in some sort of JS code.

```zsh
┌──(kali㉿kali)-[~/Downloads]
└─$ echo dmFyIGV2ZW50cyA9IFs2OCwgNjcsIDY3LCA4NCwgNzAsIDIxOSwgNzQsIDgzLCAxODksIDcwLCA0OSwgNjUsIDcxLCAyMjFdCg== | base64 -d
var events = [68, 67, 67, 84, 70, 219, 74, 83, 189, 70, 49, 65, 71, 221]
                                                                                     
┌──(kali㉿kali)-[~/Downloads]
└─$ 
```

Guessing from the name, the codes look like javascript event codes. Comparing the codes we can find the characters and get the flag.

[Source](https://www.toptal.com/developers/keycode/table)

> Flag: DCCTF{JS-F1AG}

## Bring Back from the Dead

The file contains ext4 file system data. Strings on the file shows some sort of flag.png but mounting the system suggests someone deleted the file.

```zsh
┌──(kali㉿kali)-[~/Downloads]
└─$ file challenge.img 
challenge.img: Linux rev 1.0 ext4 filesystem data, UUID=8b9adc3a-c979-4089-ac60-780ac033ed72 (needs journal recovery) (extents) (64bit) (large files) (huge files)

┌──(kali㉿kali)-[~/Downloads]
└─$ strings challenge.img  | head
/home/aryan/dcCTF/challenges/Bring Back from the Dead/mnt_loop
85@R
=h<}
readme
lost+found
flag.png
/home/aryan/dcCTF/challenges/Bring Back from the Dead/mnt_loop
6mW{
flag.png
readme
                                                                                     
┌──(kali㉿kali)-[~/Downloads]
└─$ mkdir mnt; sudo mount challenge.img mnt
                                                                             
┌──(kali㉿kali)-[~/Downloads]
└─$ cd mnt
                                                                                     
┌──(kali㉿kali)-[~/Downloads/mnt]
└─$ ls
readme
                                                                                     
┌──(kali㉿kali)-[~/Downloads/mnt]
└─$ cat readme   
Hmm wonder what happened here, did someone delete everything?
                                                                                     
┌──(kali㉿kali)-[~/Downloads/mnt]
└─$ 
```

To recover the deleted png file, we use photorec.

```zsh
┌──(kali㉿kali)-[~/Downloads]
└─$ photorec challenge.img
PhotoRec 7.2, Data Recovery Utility, February 2024
Christophe GRENIER <grenier@cgsecurity.org>
https://www.cgsecurity.org
                                                                                     
┌──(kali㉿kali)-[~/Downloads]
└─$ cd recup_dir.1 
                                                                                     
┌──(kali㉿kali)-[~/Downloads/recup_dir.1]
└─$ ls
f0008194.png  f0017410.png  report.xml
                                                                                     
┌──(kali㉿kali)-[~/Downloads/recup_dir.1]
└─$ 
```

![f0008194.png](f0008194.png?raw=true "f0008194.png")

> Flag: dcCTF{f1l3_s0rc3r0r}

## Binary Directory

Unzipping the file, we have a weird directory structure where each alphabet folder has 2 folders - 0 and 1 which then recursively contain 0 and 1 for 7 more levels which then contain a tof file which has either a 0 or 1.

```zsh
┌──(kali㉿kali)-[~/Downloads]
└─$ file chal.tar.xz 
chal.tar.xz: XZ compressed data, checksum CRC64
                                                                                     
┌──(kali㉿kali)-[~/Downloads]
└─$ tar -xJf chal.tar.xz
                                                                                     
┌──(kali㉿kali)-[~/Downloads]
└─$ ls
a  c            d  f  h  j  l  n  p  r  t  v  x
b  chal.tar.xz  e  g  i  k  m  o  q  s  u  w
                                                                                    
┌──(kali㉿kali)-[~/Downloads]
└─$ cd a/0/1/1/1/0/0/0/0 
                                                                                     
┌──(kali㉿kali)-[~/…/0/0/0/0]
└─$ ls
tof
                                                                                     
┌──(kali㉿kali)-[~/…/0/0/0/0]
└─$ cat tof             
0                                                                                     
┌──(kali㉿kali)-[~/…/0/0/0/0]
└─$ 
```

We probably have to get hold of the paths containing the tofs containing 1s and then decode them to obtain the flag. The following bash one-liner does the job.

```zsh
┌──(kali㉿kali)-[~/Downloads]
└─$ grep -r 1 | sort | cut -d ':' -f1 | cut -d '/' -f2-9 | sed "s/\///g"
01100100
01100011
01000011
01010100
01000110
01111011
01110011
01100011
01110010
00110001
01110000
00110111
00110001
01101110
01100111
01011111
00110001
01110011
01011111
01100011
00110000
00110000
01101100
01111101
                                                                                     
┌──(kali㉿kali)-[~/Downloads]
└─$ 
```

Simply decoding the following binary output gives the flag.

![binary.png](binary.png?raw=true "binary.png")

> Flag: dcCTF{scr1p7ing_1s_c00l}
