#!/usr/bin/env python3

import math
from util import to_human_readable_size
from svg.shapes import Rect
from svg.component import Text, Title, Style
from svg.container import Svg, Group

page_height = 20
page_width = 300

base_position_x = 200
address_position_x = base_position_x - 140
mode_position_x = base_position_x + page_width + 20
size_position_x = mode_position_x + 40
rss_position_x = size_position_x + 80
swap_position_x = rss_position_x + 80
pathname_position_x = swap_position_x + 80
position_y = 10

total_size, total_rss, total_swap = 0, 0, 0

mmap_svg = Svg()
global_style = Style().set_value('.func_g:hover { stroke:black; stroke-width:0.5; cursor:pointer; }')
global_style.append_value('\n').append_value('.free {fill:#999999; }')
mmap_svg.add_child(global_style)


def mmap_height(mmap):
    # min 20, max 80
    pages = mmap.space_size() / 1024 / 4
    if pages < 256:  # 256 * 4096 = 1MB
        pages = 1
    elif pages <= 262144:  # 262144 * 4096 = 1GB
        pages = 2
    elif pages < 262144 * 256:
        pages = 3
    else:
        pages = 4
    return pages * page_height


def sub_map_height(_mmap, sub_map, parent_height):
    return parent_height * round(sub_map.space_size() / float(_mmap.space_size()), 2)


def select_fill(memory_range):
    if memory_range.free:
        return "#C0C0C0"
    elif 'Java Heap' in memory_range.category:
        return "#008000"
    elif 'Class' in memory_range.category:
        return "#808000"
    elif 'Thread' in memory_range.category:
        return "#00FFFF"
    elif 'Code' in memory_range.category:
        return "#800000"
    elif 'GC' in memory_range.category:
        return "#FFFF00"
    elif 'Compiler' in memory_range.category:
        return "#800080"
    elif 'Internal' in memory_range.category:
        return "#FF00FF"
    elif 'Symbol' in memory_range.category:
        return "#000080"
    return "#008080"


def center_position_y(base_position_y, _height):
    return base_position_y + (_height - 10) / 2 + 10


def draw_header():
    global position_y
    mmap_svg.add_child(Text(base_position_x, position_y + 10, 'Memory Mapping').font_size(12))
    mmap_svg.add_child(Text(mode_position_x, position_y + 10, 'Mode').font_size(12))
    mmap_svg.add_child(Text(size_position_x, position_y + 10, 'Size').font_size(12))
    mmap_svg.add_child(Text(rss_position_x, position_y + 10, 'Rss').font_size(12))
    mmap_svg.add_child(Text(swap_position_x, position_y + 10, 'Swap').font_size(12))
    mmap_svg.add_child(Text(pathname_position_x, position_y + 10, 'Pathname').font_size(12))
    position_y = position_y + 20


def draw_mmap(idx, mmap):
    global position_y

    group = Group().attr("class", "func_g")
    mmap_svg.add_child(group)

    # title
    group.add_child(Title(mmap.start_address))

    # address text
    address_text = Text(address_position_x, position_y + 10, format_address(mmap.start_address)).font_size(12)
    group.add_child(address_text)

    # sub map
    _height, sub_elements = draw_sub_map(mmap)

    # map rect
    if _height == 0:
        _height = mmap_height(mmap)
    rect = Rect(base_position_x, position_y, page_width, _height).fill(select_fill(mmap))
    group.add_child(rect)
    for sub_ele in sub_elements:
        group.add_child(sub_ele)

    if not mmap.free:
        for ele in draw_used_info(mmap, _height):
            group.add_child(ele)

    if mmap.free:
        category_text = Text(base_position_x + 50, center_position_y(position_y, _height),
                             'Free').font_size(12)
        group.add_child(category_text)
        size_text = Text(base_position_x + 150, center_position_y(position_y, _height),
                         to_human_readable_size(mmap.space_size(), 2)).font_size(12)
        group.add_child(size_text)

    position_y = position_y + _height + 1


def draw_sub_map(mmap):
    sub_elements = []
    sub_position_y = position_y
    for sub_map in mmap.sub_maps:
        sub_height = mmap_height(sub_map)
        sub_rect = Rect(base_position_x, sub_position_y, page_width, sub_height).fill(select_fill(sub_map))
        category_text = Text(base_position_x + 50, center_position_y(sub_position_y, sub_height),
                             sub_map.category).font_size(12)
        reserve_size_text = Text(base_position_x + 150, center_position_y(sub_position_y, sub_height),
                                 to_human_readable_size(sub_map.space_size(), 2)).font_size(12)
        address_text = Text(address_position_x, sub_position_y + 10,
                            format_address(sub_map.start_address)).font_size(12)
        sub_elements.append(address_text)
        sub_elements.append(sub_rect)
        sub_elements.append(category_text)
        sub_elements.append(reserve_size_text)
        sub_position_y = sub_position_y + sub_height + 0.5
    return sub_position_y - position_y, sub_elements


def draw_used_info(mmap, _height):
    eles = []
    # size
    size_text = Text(size_position_x, center_position_y(position_y, _height),
                     to_human_readable_size(mmap.space_size(), 2)).font_size(12)
    eles.append(size_text)

    # mode
    mode_text = Text(mode_position_x, center_position_y(position_y, _height), mmap.mode).font_size(12)
    eles.append(mode_text)

    # rss
    rss_text = Text(rss_position_x, center_position_y(position_y, _height),
                    to_human_readable_size(mmap.rss, 2)).font_size(12)
    eles.append(rss_text)

    # swap
    rss_text = Text(swap_position_x, center_position_y(position_y, _height),
                    to_human_readable_size(mmap.swap, 2)).font_size(12)
    eles.append(rss_text)

    # pathname
    pathname_text = Text(pathname_position_x, center_position_y(position_y, _height),
                         mmap.get_pathname()).font_size(12)
    eles.append(pathname_text)

    # summarize
    global total_size, total_rss, total_swap
    total_size = total_size + mmap.space_size()
    total_rss = total_rss + mmap.rss
    total_swap = total_swap + mmap.swap
    return eles


def draw_summarize():
    global position_y
    mmap_svg.add_child(Text(size_position_x, position_y + 20, to_human_readable_size(total_size, 2)).font_size(12))
    mmap_svg.add_child(Text(rss_position_x, position_y + 20, to_human_readable_size(total_rss, 2)).font_size(12))
    mmap_svg.add_child(Text(swap_position_x, position_y + 20, to_human_readable_size(total_swap, 2)).font_size(12))
    position_y = position_y + 30


def format_address(address):
    return "0x" + str(address).upper().zfill(16)


def draw_mmaps(mmaps):
    draw_header()
    for i in range(len(mmaps)):
        draw_mmap(i, mmaps[i])
    draw_summarize()
    mmap_svg.attr("width", 1200)
    mmap_svg.attr("height", position_y)
    mmap_svg.view_box(0, 0, 1200, position_y)
    mmap_svg.write_to_file("mmap.svg")
