#!/usr/bin/env python3

import sys
from util import to_bytes
from util import to_human_readable_size
from mmapsvg import draw_mmaps
from memoryrange import MemoryRange


mmap_attrs = {
    "Size": "size",
    "KernelPageSize": "kernel_page_size",
    "MMUPageSize": "mmu_page_size",
    "Rss": "rss",
    "Pss": "pss",
    "Shared_Clean": "shared_clean",
    "Shared_Dirty": "shared_dirty",
    "Private_Clean": "private_clean",
    "Private_Dirty": "private_dirty",
    "Referenced": "referenced",
    "Anonymous": "anonymous",
    "LazyFree": "lazy_free",
    "AnonHugePages": "anon_huge_pages",
    "ShmemPmdMapped": "shmem_pmd_mapped",
    "Shared_Hugetlb": "shared_hugetlb",
    "Private_Hugetlb": "private_hugetlb",
    "Swap": "swap",
    "SwapPss": "swap_pss",
    "Locked": "locked",
    "THPeligible": "tH_peligible",
    "VmFlags": "vm_flags",
}


class MemoryMapping(MemoryRange):
    """memory mapping"""
    start_address = ''
    end_address = ''
    mode = ''
    offset = 0
    inode = 0
    pathname = ''
    size = 0
    kernel_page_size = 0
    mmu_page_size = 0
    rss = 0
    pss = 0
    shared_clean = 0
    shared_dirty = 0
    private_clean = 0
    private_dirty = 0
    referenced = 0
    anonymous = 0
    lazy_free = 0
    anon_huge_pages = 0
    shmem_pmd_mapped = 0
    shared_hugetlb = 0
    private_hugetlb = 0
    swap = 0
    swap_pss = 0
    tH_peligible = 0
    vm_flags = ''

    def __init__(self, category, start_address, end_address):
        super().__init__(category, start_address, end_address)
        self.sub_maps = []
        self.pathname = ''

    def pages(self):
        return int((int(self.end_address, 16) - int(self.start_address, 16)) / self.kernel_page_size)

    def add_sub_map(self, memory_range):
        self.sub_maps.append(memory_range)
        self.sub_maps = sorted(self.sub_maps, key=lambda m_range: m_range.start_bytes())

    def get_pathname(self):
        if self.pathname != '':
            return self.pathname
        else:
            return "[anonymous]"

def parse_mmap(lines):
    mmap = None
    for idx, line in enumerate(lines):
        # print(line, end='')
        if idx == 0:
            fields = line.split()
            mmap = MemoryMapping('', fields[0].split('-')[0], fields[0].split('-')[1])
            mmap.mode = fields[1]
            mmap.offset = fields[2]
            mmap.inode = fields[4]
            if len(fields) == 6:
                mmap.pathname = fields[5]
        else:
            fields = line.split(':')
            if fields[0] == 'THPeligible' or fields[0] == 'VmFlags':
                setattr(mmap, mmap_attrs[fields[0]], fields[1].strip())
            else:
                setattr(mmap, mmap_attrs[fields[0]], to_bytes(fields[1]))
    return mmap


def padding_mmaps(mmaps):
    # mmaps = sorted(mmaps, key=lambda mmap: mmap.start_address_byte())
    mmaps = sorted(mmaps, key=lambda mmap: mmap.start_bytes())
    result = []
    _cur_start_address = '0000'
    for cur_mmap in mmaps:
        if _cur_start_address != cur_mmap.start_address:
            free_mmap = MemoryMapping('', _cur_start_address, cur_mmap.start_address)
            free_mmap.kernel_page_size = cur_mmap.kernel_page_size
            free_mmap.free = True
            result.append(free_mmap)
        result.append(cur_mmap)
        _cur_start_address = cur_mmap.end_address
    return result


def parse_smaps_file(file):
    _memory_maps = []
    mmap_lines = []
    with open(file) as fp:
        for cnt, line in enumerate(fp):
            mmap_lines.append(line)
            if line.startswith("VmFlags"):
                _memory_maps.append(parse_mmap(mmap_lines))
                mmap_lines = []
    return padding_mmaps(_memory_maps)


def format_line(args):
    return '{:<30} {:<35} {:<15} {:<8} {:<8} {:<10} {:<8} {:<15}'.format(*args)


if __name__ == '__main__':
    memory_maps = parse_smaps_file(sys.argv[1])
    print(f'Total {len(memory_maps)} mappings. '
          f'page size = {to_human_readable_size(memory_maps[0].kernel_page_size, 0)}')
    print(format_line(['address', 'address', 'start_address', 'size', 'pages', 'rss', 'mode', 'pathname']))
    for i in range(len(memory_maps)):
        _mmap = memory_maps[i]
        print(format_line([f'{_mmap.start_address} - {_mmap.end_address}',
                           f'{int(_mmap.start_address, 16)} - {int(_mmap.end_address, 16)}',
                           to_human_readable_size(int(_mmap.start_address, 16), 2),
                           to_human_readable_size(_mmap.size, 2),
                           _mmap.pages(),
                           to_human_readable_size(_mmap.rss, 0), _mmap.mode, _mmap.pathname]))
    # draw_mmaps(memory_maps)
