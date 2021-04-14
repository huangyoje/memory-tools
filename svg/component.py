#!/usr/bin/env python3

from svg.baseelement import BaseElement


class Text(BaseElement):

    element_name = 'text'

    def __init__(self, x, y, value):
        super().__init__()
        self.value = value
        self.attr("font-family", "Verdana").attr("fill", "rgb(0,0,0)")
        self.attr("x", x).attr("y", y)

    def font_size(self, value):
        self.attr("font-size", value)
        return self

    def font_family(self, value):
        self.attr("font-family", value)


class Title(BaseElement):

    element_name = 'title'

    def __init__(self, value):
        super().__init__()
        self.value = value


class Style(BaseElement):
    element_name = 'style'

    def __init__(self):
        super().__init__()
        self.attr("type", "text/css")
