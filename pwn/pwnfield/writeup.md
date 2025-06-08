## Pwnfield Writeup

### Description

We discovered that PwnTopia use their secret mine to collect _shellcodium_, a very rare and powerful resource!
We need it too, to be able to defend N0PStopia. However, PwnTopia has put some mines in the way to the _shellcodium_, but we are lucky PwnTopia left their most powerful tool,a shell, _sh_ on their way out! Can this be a secret message? Can you manage to avoid the mines and use their tool against them?

**Author: Xen0s**

### Solution

The code still has some comments, that might help the users. The program implants "mines", basically exit instructions. The problem is, with normal flow, it is unavoidable to hit a mine. But +1 index in memory allows to choose an arbitrary location, even though limited. Inputting 33 as the index, the program contunies flow from second byte of the second mov operation the user provides. Here it is clear that the user has maximum of 4 bytes, as first byte always does the mov operation. The user can construct a shellcode as follows:
|mov|x|x|j|j|
Mine
|mov|x|x|j|j|
Mine
|mov|x|x|j|j|

And the code will triggered as second byte is the beginning of the flow: 
|mov|o|x|j|j|
Mine
|mov|x|x|j|j|
Mine
|mov|x|x|j|j|

x is critical code that carries the shellcode, j is relative jump that only uses 2 bytes and o is the entry point. So, the user is needed to write a shellcode that executes 2 bytes maximum per instruction. It is clear that no immediate value can be loaded, so it is needed to analyze the current state using GDB. Here, the idea is to get a shell via sh link using execve syscall.

Following operations set up the registers and calls exec syscall:

```asm
xor edx, edx # null out params for execve
xor esi, esi # null out params for execve
mov al, 0x73 # letter s
mov ah, 0x68 # letter h
push rax, push rsp # Push "sh" to stack and record where it is through stack
pop rdi # Pop the address of "sh" to point it for execve
xor eax, eax # clear eax as it had "sh" before
mov al, 0x3b # move execve syscall number to rax
syscall
```

We use 32 bit registers in some places as 64 bit operations generally use 3 bytes for operations and it breaks the flow. Some registers are conveniently already 0, or carry information on the least significant 32 bits, so we can just use xor of 32 bit registers.

The code calls a shell, through the link to /bin/sh, using the file sh (as mentioned in the hints), so the user can cat the flag. This was intended to make the challenge easier to solve, as the filename is 2 bytes long. It should still be possible to do without, via using 2 stage payload to read code into memory then execute.

Flag : `N0PS{0n3_h45_70_jump_0n_7h3_204d_70_pwnt0p1a}`