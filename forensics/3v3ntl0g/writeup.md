## 3v3ntl0g

### Description

We were able to infiltrate a WebTopia server!
However, our hacking skills are not very good... We were only able to read from the keyboard input driver.
Here is the data we collected, can you have a look? It seems that is has been shuffled a bit though...
Also, WebTopia freaks are frenchies, and they use an AZERTY keyboard, just in case you need that information...

**Author: algorab**

### Solution

We are facing a binary data file that is a raw keyboard input read from the `/dev/input/eventXX` file. Therefore, we have to read the raw data.
According to the [`input.h`](https://github.com/torvalds/linux/blob/master/include/uapi/linux/input.h), each inpout event is stored in a 24 bytes buffer :

```c
struct input_event {
#if (__BITS_PER_LONG != 32 || !defined(__USE_TIME_BITS64)) && !defined(__KERNEL__)
	struct timeval time;
#define input_event_sec time.tv_sec
#define input_event_usec time.tv_usec
#else
	__kernel_ulong_t __sec;
#if defined(__sparc__) && defined(__arch64__)
	unsigned int __usec;
	unsigned int __pad;
#else
	__kernel_ulong_t __usec;
#endif
#define input_event_sec  __sec
#define input_event_usec __usec
#endif
	__u16 type;
	__u16 code;
	__s32 value;
};
```

The first two packs of 64 bits are the timestamp of the event. The next 16 bits represent the `type` of the event, then 16 bits for its `code`, and then the last 32 bits are the `value` of the event.

The different types of events can be found in the [`input-event-codes.h`](https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h) file. Here, we will be looking for `EV_KEY` event, which represents a pressed key.

The `code` represents the value of the key that was pressed. All values can be found in the [`input-event-codes.h`](https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h) too.

Finally, the `value` indicates if the key was pressed or released. `1` is for a pressed key and `0` for a released one.

Given all those elements, we can write a script that will read the data, sort the different events based on their timestamps, and then decode them in order to retrieve the flag.

```python
import struct

map = {
    2: "1",
    3: "2",
    4: "3",
    5: "4",
    6: "5",
    7: "6",
    8: "7",
    9: "8",
    10: "9",
    11: "0",
    13: "=",
    16: "Q",
    17: "W",
    18: "E",
    19: "R",
    20: "T",
    21: "Y",
    22: "U",
    23: "I",
    24: "O",
    25: "P",
    28: "[ENTER]",
    29: "[CTRL]",
    30: "A",
    31: "S",
    32: "D",
    33: "F",
    34: "G",
    35: "H",
    36: "J",
    37: "K",
    38: "L",
    39: ";",
    40: "'",
    42: "[SHIFT]",
    44: "Z",
    45: "X",
    46: "C",
    47: "V",
    48: "B",
    49: "N",
    50: "M",
    51: ",",
    52: ".",
    53: "/",
    100: "[ALT]",
    103: "[UP]"
}

input = open("shuffled.bin", 'rb')
events = []
buff = input.read(24)

while buff:

    (uts, msec, typ, code, value) = struct.unpack('llhhi', buff)

    events.append({
        "ts": uts+msec*10**(-6),
        "typ": typ,
        "code": code,
        "value": value
    })
    buff = input.read(24)

events = sorted(events, key=lambda d: d["ts"])

for event in events:

    if event["typ"] == 1:
        if event["value"] == 1:
            print(f"{map[event['code']]} pressed.")
        elif event["value"] == 0:
            print(f"{map[event['code']]} released.")
```

By running this script, we can then recover the keys that were pressed, and from that recover the flag.

### Flag

`N0PS{c4n_y0U_R34d_Th15??}`