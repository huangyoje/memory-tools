#!/usr/bin/env python3

import sys
import re
from util import to_human_readable_size
from memoryrange import MemoryRange


class JvmNativeMemoryCategory(MemoryRange):

    def __init__(self, category, start_address, end_address):
        super().__init__(category, start_address, end_address)
        self.reserved = MemoryRange('', start_address, end_address)
        self.committed = []

    def commit(self, start_address, end_address):
        # self.committed.append(MemoryRange('', start_address, end_address))
        pass

    def update_start_address(self, new_start_address):
        new_category = JvmNativeMemoryCategory(self.category, new_start_address, self.end_address)
        # for
        return new_category

    def update_end_address(self, new_end_address):
        new_category = JvmNativeMemoryCategory(self.category, self.start_address, new_end_address)
        # for
        return new_category

    def update_address(self, new_start_address, new_end_address):
        new_category = JvmNativeMemoryCategory(self.category, new_start_address, new_end_address)
        # for
        return new_category

    def __str__(self):
        return f'{self.category:<15}  reserved {self.reserved}'


def parse_native_memory_category(lines):
    # print("********************")
    for idx, line in enumerate(lines):
        # [0x00007ffff7f6f000 - 0x00007ffff7fef000] reserved and committed 512KB for Thread Stack from
        _match = re.search('\\[0x(.+) - 0x(.+)] reserved and committed (.+) for (.+) from', line)
        if _match:
            _category = JvmNativeMemoryCategory(_match.group(4), _match.group(1), _match.group(2))
            _category.commit(_match.group(1), _match.group(2))
            return _category;
        # [0x00000000f8000000 - 0x0000000100000000] reserved 131072KB for Java Heap from
        _match = re.search('\\[0x(.+) - 0x(.+)] reserved (.+) for (.+) from', line)
        if _match:
            _category = JvmNativeMemoryCategory(_match.group(4), _match.group(1), _match.group(2))
        # 	[0x0000000100000000 - 0x0000000100080000] committed 512KB from
        _match = re.search('\\[0x(.+) - 0x(.+)] committed (.+) from', line)
        if _match:
            _category.commit(_match.group(1), _match.group(2))
    return _category


def parse_nmt_detail(file):
    _jvm_native_memory_categories = []
    _category_lines = []
    _memory_map_flag = False
    with open(file) as fp:
        for cnt, line in enumerate(fp):
            if line.startswith("Virtual memory map"):
                _memory_map_flag = True
                continue
            if line.startswith("Details"):
                if len(_category_lines) > 0:
                    _jvm_native_memory_categories.append(parse_native_memory_category(_category_lines))
                break
            if _memory_map_flag:
                if line.startswith("[0x") and "] reserved " in line:
                    if len(_category_lines) > 0:
                        _jvm_native_memory_categories.append(parse_native_memory_category(_category_lines))
                        _category_lines = []
                    _category_lines.append(line)
                if "] committed " in line and " from" in line:
                    _category_lines.append(line)
    return _jvm_native_memory_categories


if __name__ == '__main__':
    categories = parse_nmt_detail(sys.argv[1])
    print('\n\n'.join(map(str, categories)))
