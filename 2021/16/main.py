import numpy as np
import math

with open("./input.txt") as f:
    buf = bytes.fromhex(f.read().strip())
    packet = np.unpackbits(np.frombuffer(buf, dtype=np.uint8))

def to_int(bits):
    n = 0
    for i in range(len(bits)):
        n += bits[i] << len(bits) - i - 1
    return n

class Packet:
    def __init__(self, bits):
        self.version = to_int(bits[0:3])
        self.id = to_int(bits[3:6])
        self.number = None
        self.packets = []
        self.length = 6
        # literal number
        if self.id == 4:
            idx = 6
            buf = np.empty((0,), dtype=np.uint8)
            while bits[idx] == 1:
                buf = np.append(buf, bits[idx+1:idx+5])
                idx += 5
                self.length += 5
            buf = np.append(buf, bits[idx+1:idx+5])
            self.length += 5
            self.number = to_int(buf)
            return
        # sub packet bit length
        if bits[6] == 0:
            bit_len = to_int(bits[7:22])
            idx = 22
            self.length += 1 + 15 + bit_len
            while bit_len > 0:
                p = Packet(bits[idx:idx+bit_len])
                self.packets.append(p)
                bit_len -= p.length
                idx += p.length
        # sub packet length
        elif bits[6] == 1:
            sub_len = to_int(bits[7:18])
            idx = 18
            self.length += 1 + 11
            for _ in range(sub_len):
                p = Packet(bits[idx:])
                self.packets.append(p)
                self.length += p.length
                idx += p.length

    @property
    def total_version(self):
        v = self.version
        for p in self.packets:
            v += p.total_version
        return v

    @property
    def value(self):
        if self.id == 0:
            return sum([p.value for p in self.packets])
        elif self.id == 1:
            return math.prod([p.value for p in self.packets])
        elif self.id == 2:
            return min([p.value for p in self.packets])
        elif self.id == 3:
            return max([p.value for p in self.packets])
        elif self.id == 4:
            return self.number
        elif self.id == 5:
            return 1 if self.packets[0].value > self.packets[1].value else 0
        elif self.id == 6:
            return 1 if self.packets[0].value < self.packets[1].value else 0
        elif self.id == 7:
            return 1 if self.packets[0].value == self.packets[1].value else 0


p = Packet(packet)
print("Answer 1:", p.total_version)
print("Answer 2:", p.value)
