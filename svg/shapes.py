#!/usr/bin/env python3

from svg.baseelement import BaseElement


class Rect(BaseElement):

    element_name = 'rect'

    def __init__(self, x, y, width, height):
        super().__init__()
        self.attr("x", x).attr("y", y).attr("width", width).attr("height", height)

    def fill(self, color):
        self.attr("fill", color)
        return self
