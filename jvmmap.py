#!/usr/bin/env python3

import argparse
from epmap import parse_smaps_file
from jvmnmt import parse_nmt_detail
from util import to_human_readable_size
from mmapsvg import draw_mmaps

# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('--smaps', type=str, help='/proc/pid/smaps file')
parser.add_argument('--nmt', type=str, help='jvm native memory track detail file')
args = parser.parse_args()


def merge_maps(pmaps, nmt_maps):
    for nmt_map in nmt_maps:
        add_sub_map(pmaps, nmt_map)


def add_sub_map(pmaps, nmt_map):
    for pmap in pmaps:
        if pmap.contains(nmt_map):
            # print(f'[{pmap.start_address}, {pmap.end_address}] contains [{nmt_map.start_address}, {nmt_map.end_address}]')
            pmap.add_sub_map(nmt_map)
        elif pmap.contain_by(nmt_map):
            # print(
            #     f'[{pmap.start_address}, {pmap.end_address}] contain by [{nmt_map.start_address}, {nmt_map.end_address}]')
            pmap.add_sub_map(nmt_map.update_address(pmap.start_address, pmap.end_address))
        elif pmap.left_join(nmt_map):
            # print(
            #     f'[{pmap.start_address}, {pmap.end_address}] left join [{nmt_map.start_address}, {nmt_map.end_address}]')
            pmap.add_sub_map(nmt_map.update_start_address(pmap.start_address))
        elif pmap.right_join(nmt_map):
            # print(
            #     f'[{pmap.start_address}, {pmap.end_address}] right join [{nmt_map.start_address}, {nmt_map.end_address}]')
            pmap.add_sub_map(nmt_map.update_end_address(pmap.end_address))


def parse_maps():
    memory_maps = parse_smaps_file(args.smaps)
    nmt_maps = parse_nmt_detail(args.nmt)
    merge_maps(memory_maps, nmt_maps)
    # for i in range(150):
    #     _mmap = memory_maps[i]
    #     print(format_line([_mmap.start_address,
    #                        _mmap.end_address,
    #                        _mmap.pages(),
    #                        to_human_readable_size(_mmap.rss, 0),
    #                        _mmap.mode,
    #                        _mmap.pathname]))
    #     for sub_map in  _mmap.sub_maps:
    #         print(f'    {sub_map}')
    # for i in range(3):
    #     nmt_map = nmt_maps[i]
    #     print(nmt_map)
    return memory_maps


#     |    |       base
#  | |             no
#  |  |            no
#  |    |          left_join
#  |       |       containBy
#  |          |    containBy
#     | |          contains
#     |     |      equals
#     |       |    containBy
#      |  |        contains
#      |    |      contains
#      |      |    right_join
#           | |    no
#            ||    no
#


def format_line(_args):
    return '{:<10} {:<10} {:<8} {:<8} {:<8} {:<10}'.format(*_args)


def output_svg(mmaps):
    draw_mmaps(mmaps)


if __name__ == '__main__':
    output_svg(parse_maps())
