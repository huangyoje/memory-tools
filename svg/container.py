#!/usr/bin/env python3

from svg.baseelement import BaseElement


class Svg(BaseElement):

    element_name = 'svg'

    def __init__(self):
        super().__init__()
        self.attr("xmlns", "http://www.w3.org/2000/svg")
        self.attr("xmlns:xlink", "http://www.w3.org/1999/xlink")
        self.attr("version", "1.1")

    def view_box(self, min_x, min_y, x, y):
        self.attr("viewBox", f'{min_x}, {min_y}, {x}, {y}')
        return self

    def write_to_file(self, filename):
        with open(filename, "w") as text_file:
            text_file.write(self.to_string())


class Group(BaseElement):

    element_name = 'g'

    def __init__(self):
        super().__init__()
        self.attr("style", "display: block; opacity: 1;")
