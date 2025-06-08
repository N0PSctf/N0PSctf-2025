## A515

### Description

We just received this sign from Foreniego, one of the wanderers of Pwntopia.
He's known for drifting between Topias, never settling down, and always leaving behind a few secrets.
We've been told there's something hidden in the sign he sent us, maybe it holds a clue that will help in the steps ahead.
Can you uncover the truth he's hiding?

**Authors: y3noor & Sto**

### Solution

The image is a [PNG](https://en.wikipedia.org/wiki/PNG). Initially, the image file seems fine. Some basic checks don't raise any sign of file corruption, hidden information or whatsoever. However, after analyzing the file a bit, we can see that the number of IDAT chunks is quite big, and that some of the chunks are not used.
Therefore, we can try to recreate an image by taking only one IDAT chunk at a time and recombine them in a different order!
Here is the script that allows to do it:

```python
data = open("BLUE.png", 'rb').read()

header = b""
chunks = []
footer = b""
is_first_idat = True

for i in range(len(data)-4):
    if data[i:i+4] == b"IDAT":
        if is_first_idat:
            is_first_idat = False
            header = header[:-4]
        size = int.from_bytes(data[i-4:i], byteorder="big")
        chunk = data[i-4:i+4+size+4]
        chunks.append(chunk)
    if data[i:i+4] == b"IEND":
        footer = data[i-4:]
    if is_first_idat:
        header += bytes([data[i]])

chunks_order = [11, 12, 10, 14, 16, 15, 17, 18, 8, 13, 9]

for i in range(len(chunks)):
    if not i in chunks_order:
        with open(f"out{i}.png", "wb") as out:
            out.write(header)
            for index in chunks_order:
                out.write(chunks[index])
            out.write(chunks[i])
            out.write(footer)
```

With this script, starting with `chunks_order = []`, we can at each iteration add a chunk to the list, corresponding to the chunk that adds a part to the image. In the end, we end up with the list that is in the script. Finally, we get a totally different image, with Foreniego holding a sign with the flag!

![Output image](./assets/out.png)

### Flag

`N0PS{1M4G3_r3C0nsTRuc7i0n}`