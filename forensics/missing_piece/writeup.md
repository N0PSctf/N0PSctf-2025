## Missing Piece

### Description

We managed to steal this USB stick from a member of PwnTopia, but there was nothing useful on it.
Can you see if you can find anything ?

**Authors: algorab, CaptWake**

### Solution

#### Challenge Overview
The challenge provides a corrupted .img disk image file that cannot be mounted. The goal is to recover data from the image, potentially by analyzing its partition structure, extracting files, and decrypting hidden content to reveal the flag.

#### Initial Analysis
Since the disk image is corrupted and unmountable, forensic tools are needed to inspect its structure and recover data. We used The Sleuth Kit (TSK) to analyze the partition table with 
the `mmls` command:

```powershell
> mmls.exe disk.img
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors
      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000002047   0000002048   Unallocated
002:  000:000   0000002048   0002078719   0002076672   Win95 FAT32 (0x0b)
003:  -------   0002078720   0002099199   0000020480   Unallocated
```
The output reveals a `Win95 FAT32` partition:
- `Start Sector`: 2048
- `End Sector`: 2078719
- `Length`: 2076672 sectors

This partition is likely where the relevant data resides.

#### File System Exploration
To list the files within the `FAT32` partition, I used TSK’s `fls` command with the partition offset (`-o 2048`):
```powershell
> fls.exe -o 2048 disk.img
r/r 3:	USB Drive   (Volume Label Entry)
r/r * 6:	cryptodisko.passwd
r/r * 8:	cryptodisko
v/v 33161379:	$MBR
v/v 33161380:	$FAT1
v/v 33161381:	$FAT2
V/V 33161382:	$OrphanFiles
```

Two files are marked as deleted, however their content can still be in the provided disk image:

- `cryptodisko`: Likely an executable responsible for encryption/decryption.
- `cryptodisko.passwd`: Potentially contains a key or password.

We can try extract to recover the content of these files using TSK’s `tsk_recover` command:
```powershell
> tsk_recover.exe -o 2048 disk.img 
```

#### Analyzing the Files

The `cryptodisko.passwd` file contains the string: `PwnT0p14_s3cr3t_p4rt1t10n`
This 25-byte string is likely the encryption key used by cryptodisko.

`cryptodisko` Binary
The cryptodisko file is a Go ELF binary. Running it with the `-h` flag provides usage information:

```bash
> ./cryptodisko -h
Usage of ./cryptodisko:
  -d string
        Name of the disk to work on
  -h int
        Size of the hidden partition in bytes (default 10485760)
  -k string
        Key for the encryption/decryption
  -m string
        Specify a mode among "create" and "encrypt"
```

The binary supports two modes:
- `create`: Likely sets up a hidden partition.
- `encrypt`: Encrypts data on the disk using a provided key.

Given the presence of `cryptodisko.passwd`, the disk image was likely encrypted using the key `PwnT0p14_s3cr3t_p4rt1t10n`. The next step is to reverse-engineer the binary to understand the encryption mechanism.

#### Reversing cryptodisko binary

After firing up IDA to analyze the Go binary we see that the symbols were not stripped, making it easier to identify custom code versus third-party Go modules. 

The first function that caught our attention was `main_main_crypt_part`, this is responsible for encrypting the partition has the name suggests. We can see that instead of looping through each partition, the program simply encrypt the last one using the key provided as input and an IV using `AES-256-CBC`.

```asm
call    main_get_partitions
test    rdi, rdi
jnz     loc_4C8543
lea     rdx, [rbx-1] ;  rbx stores the number of partitions
cmp     rbx, rdx     ;
jbe     loc_4C855A
```

Unfortunately the decompiled code of IDA is not very helpful when decompiling golang functions. Here is the disasm code responsible in reading the partition content: 
```asm
mov rdi, [rsp+98h+p]; Loads the size.
mov rsi, [rsp+98h+beginBytes]; Loads the partition start offset.
mov rax, [rsp+98h+fd]; Loads the file descriptor.
call syscall_pread; Reads the partition data into the content buffer.
```

After that we can see that the program reads 16 bytes (this will be our IV) from the MBR partition entry:
```asm
mov     rax, [rsp+98h+fd] ; fd
mov     rdi, 10h        ; Load the size
mov     rsi, [rsp+98h+offset] ; Loads the offset (0x1BE + i * 16).
call    syscall_pread
```

Then the program calls `main_Aes256Encode`, if we disassemble this function, we can see that the plaintext is padded using a custom function named `main_PKCS5Padding` that basically is implementing the classic PKCS5 padding scheme.

Following the code after the padding, we can see an instruction `cmp rdx, 20h` at `0x4C7996` that checks if the key length stored in the `rdx` register is equal to 32, if that's not the case the program will first pad the key with the value `pad = 32 - len(key)` and then finally encrypts the partition.
```asm
mov     rax, [rsp+98h+IV.len] ; content
mov     rbx, [rsp+98h+p] ; content
mov     rcx, rbx        ; content
mov     rdi, [rsp+98h+path.cap] ; encryptionKey
mov     rsi, [rsp+98h+err.tab] ; encryptionKey
mov     r8, [rsp+98h+err.data] ; encryptionKey
mov     r9, [rsp+98h+IV.array] ; IV
mov     r10d, 10h       ; IV
mov     r11, r10        ; IV
call    main_Aes256Encode
```

Before writing the ciphertext back to disk, the program appends the IV at the start of the ciphertext, and zeores the MBR partition entry of the hidden partition. 

The instruction `lea rbx, [rdx+rdi]` at `0x4C7A74` computes `len(IV) + len(ciphertext)` Then the  call `runtime_memmove` at `0x4C7AD2` is responsible to copy the ciphertext after IV in the new slice. This will then be written on disk through the call `syscall_pwrite` at `0x4C8440`.

We can see another call to `syscall_pwrite` at `0x4C84FA` that in this case writes a buffer filled of zeroes stored in the `rdi` register in the MBR partition entry belonging to the hidden partition, effectively erasing it from the MBR table.

Here is the pytthon script that decrypts the encrypted partition content:  
```python
from Crypto.Cipher import AES
import struct
from sys import argv

# Original key (25 bytes) padded with 7 bytes of 0x19 to reach 32 bytes for AES-256
key = b"PwnT0p14_s3cr3t_p4rt1t10n" + b"\x19" * 7


def read_last_partition(disk_path):
    with open(disk_path, "rb") as f:
        # Seek to the start of the last partition entry (since the image contains only one partition)
        # The last partition entry is at offset 0x1BE in the MBR
        f.seek(0x1BE)
        entry = f.read(16)
        start_sector = struct.unpack("<I", entry[8:12])[0]
        start_offset = start_sector * 512
        return start_offset


def pkcs5_unpadding(padded_data):
    """
    Removes PKCS#5 padding from the given padded data.
    """
    # The last byte indicates the padding length
    padding_length = padded_data[-1]
    # Return the data with padding removed
    return padded_data[:-padding_length]


# Function to decrypt a single partition
def decrypt_partition(disk_path, start, key):
    """
    Decrypts a partition using AES-256-CBC with the provided key.
    """

    with open(disk_path, "rb") as f:
        f.seek(start)
        iv = f.read(16)
        size = struct.unpack("<I", iv[12:16])[0]
        encrypted_data = f.read(size * 512)

    # Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Decrypt and remove PKCS5 padding
    try:
        decrypted = pkcs5_unpadding(cipher.decrypt(encrypted_data))
        return decrypted
    except ValueError as e:
        print(f"Decryption failed: {e}")
        return b""


if __name__ == "__main__":
    src_disk = argv[1]
    dst_disk = argv[2]

    if len(argv) != 3:
        print(f"Usage: python {argv[0]} <src_disk> <dst_disk>")
        exit(1)

    start = read_last_partition(src_disk)
    decrypted_partition = decrypt_partition(src_disk, start, key)

    # Write decrypted data to output file
    with open(dst_disk, "wb") as f:
        f.write(decrypted_partition)
```

After running it, we searched the prefix flag through the strings of the decrypted image revealing us the full flag:

```bash
> strings disk.img.decrypted | grep -i "N0PS"
N0PS{mBr_t4bl3_h4s_n0_s3cr3t_4_U_4Nym0r3}
```

