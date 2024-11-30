#!/usr/bin/env python3

import struct
from datetime import datetime
from hashlib import sha1
from itertools import chain
from uuid import getnode


def get_ntp():
    t = datetime.now().timestamp()
    return (int(t) + 2208988800) << 32 | int((t % 1) * 2**32)


def get_eui():
    mac = struct.pack("<Q", getnode())
    eui = list(chain(mac[:3], b"\xfe\xff", mac[3:6]))
    eui[5] |= 0x2
    return struct.unpack("<Q", bytes(eui))[0]


if __name__ == "__main__":
    ntp = get_ntp()
    eui = get_eui()
    key = struct.pack("=QQ", ntp, eui)
    gid = sha1(key).digest()[15:]
    print("fd%02x:%02x%02x:%02x%02x::/64" % tuple(gid))
