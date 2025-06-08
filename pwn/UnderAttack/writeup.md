## Under Attack 

### Description

Ladybug Command System FULLY OPERATIONAL.

**Author : y3noor**

### Solution

The `ladybug_app` is a binary that uses a command-based interface to control "agents." The objective is to leak a libc address and trigger a **ROP chain** to spawn a shell.

The script begins by connecting to the binary, locally, remotely, or via GDB, and loads the ELF binary and an optional `libc.so.6`. It waits for the initial prompt: `Noopsy Land is ours! Your command, Overlord?:`.

To leak a libc address, Agent 0 is deployed with 1072 bytes and Agent 1 with 32 bytes. Agent 0 is then recalled to create a use-after-free condition. Intel is gathered from Agent 0, leaking a libc pointer. The libc base address is computed using a known offset (`0x1d2cc0`).

Next, the script resolves the addresses of `system`, `exit`, `pop rdi; ret`, and `ret` gadgets from the loaded libc. Agent 2 is deployed with 200 bytes of space, and a payload is crafted containing `/bin/sh`, alignment and argument setup, followed by a call to `system("/bin/sh")`, and a clean call to `exit`. This payload is injected using the `corrupt_systems` command and verified using `gather_intel`.

Finally, the `initiate_city_takeover` command is used to trigger execution at the payload location. If successful, the binary executes the ROP chain and spawns an interactive shell.

The full solution script can be found in the [`sol.py`](sol.py).


### Flag

The flag is `N0PS{its_N0pSt0pia's_Pleasure_that_L4dy_bug__is_w3aaker!!!__}`