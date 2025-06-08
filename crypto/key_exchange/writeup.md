## Key Exchange

### Description

We have located a secret endpoint of CrypTopia. If me manage to establish a communication with it, we should be able to get sensitive information!

**Author: algorab**

### Solution

By reading the source code, we can notive that a shared key is established between the client and the server, which is then used to encrypt the flag.
Moreover, we can notice that the key exchange protocol is [Diffie-Hellman](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange).
Therefore, we need to write a client for this server that will achieve the key exchange protocol, which will allow us to decrypt the flag with the shared key.

```python
from pwn import *
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import sys

N = 1024

s = connect(sys.argv[1], int(sys.argv[2]))

p = int.from_bytes(s.recv(N))
g = int.from_bytes(s.recv(N))
k_a = int.from_bytes(s.recv(N))
b = 2
k_b = pow(g, b, p)
s.send(k_b.to_bytes(N))
k = pow(k_a, b, p)
flag = s.recvall()

k = sha256(k.to_bytes((k.bit_length() + 7) // 8)).digest()
iv = flag[:AES.block_size]
data = flag[AES.block_size:]
cipher = AES.new(k, AES.MODE_CBC, iv)
open('decrypted', 'wb').write(unpad(cipher.decrypt(data), AES.block_size))
```

By analyzing the decrypted data, we notice this is a PNG image.

### Flag

The flag is `N0PS{d1fFi3_h31lm4n_k3y_XcH4ng3}`