#!/usr/bin/env python3

from util import to_human_readable_size


class MemoryRange(object):

    def __init__(self, category, start_address, end_address):
        self.category = category
        self.start_address = start_address
        self.end_address = end_address
        self.free = False

    def space_size(self):
        return int(self.end_address, 16) - int(self.start_address, 16)

    def __str__(self):
        return f'[{self.start_address} - {self.end_address}] size={to_human_readable_size(self.space_size(), 2)}'

    def start_bytes(self):
        return int(self.start_address, 16)

    def end_bytes(self):
        return int(self.end_address, 16)

    def contains(self, other):
        return self.start_bytes() <= other.start_bytes() and self.end_bytes() >= other.end_bytes()

    def contain_by(self, other):
        return other.contains(self)

    def left_join(self, other):
        return other.start_bytes() < self.start_bytes() < other.end_bytes() < self.end_bytes()

    def right_join(self, other):
        return self.start_bytes() < other.start_bytes() < self.end_bytes() < other.end_bytes()


if __name__ == '__main__':
    m1 = MemoryRange('', '100080000', '140000000')
    m2 = MemoryRange('', '0000000100000000', '0000000140000000')
    print(m1.contains(m2))
    print(m1.left_join(m2))
    print(m1.right_join(m2))
