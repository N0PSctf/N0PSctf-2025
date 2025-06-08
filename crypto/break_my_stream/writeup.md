## Break My Stream

### Description

CrypTopia is testing their next gen encryption algorithm. We believe that the way they implemented it may have a flaw...

**Author: algorab**

### Solution

By reading the source code, we can see that the algorithm is a stream cipher. Moreover, there is an implementation error, as the key scheduling operation and the PRNG are reinitialised before every encryption. Therefore, the keystream is always the same, and we end up with a [key reusing for every encryption](https://en.wikipedia.org/wiki/Stream_cipher_attacks#Reused_key_attack). Then, by knowing both plaintext and ciphertext, it is possible to recompute the keystream, and then recover the flag.

```python
from pwn import *

s = connect(sys.argv[1], int(sys.argv[2]))

s.recvuntil(b'thing: ')
enc_flag = bytes.fromhex(s.recvuntil(b'\n')[:-1].decode())
pt = b'\x00' * (len(enc_flag))
s.recvuntil(b': ')
s.sendline(pt)
ct = bytes.fromhex(s.recvline()[:-1].decode())
keystream = xor(ct, pt)
flag = xor(enc_flag, keystream)
print(flag)
```

### Flag

The flag is `N0PS{u5u4L_M1sT4k3S...}`