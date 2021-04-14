#!/usr/bin/env python3

"""
The base of xml element
"""


class BaseElement(object):

    element_name = 'baseElement'

    def __init__(self):
        self.attrs = dict()
        self.children = []
        self.value = ''

    def attr(self, attr, value):
        self.attrs[attr] = value
        return self

    def append_attr(self, attr, value):
        if attr in self.attrs:
            return self.attr(attr, self.attrs[attr] + value)
        else:
            return self.attr(attr, value)

    def add_child(self, element):
        self.children.append(element)
        return self

    def set_value(self, value):
        self.value = value
        return self

    def append_value(self, value):
        self.value = self.value + value
        return self

    def to_string(self):
        return self.__to_string(0)

    def __to_string(self, level):
        _str = f'{self.__padding_space(level)}<{self.element_name} {self.__attrs_to_string()}>'
        if self.children:
            # has children
            _str = _str + '\n' + self.__children_to_string(level + 1) + '\n'
            _str = _str + f'{self.__padding_space(level)}'
        if self.value:
            _str = _str + str(self.value)
        _str = _str + f'</{self.element_name}>'
        return _str

    def __attrs_to_string(self):
        return ' '.join('{}="{}"'.format(attr, value) for attr, value in self.attrs.items())

    def __children_to_string(self, level):
        return '\n'.join(map(lambda e: BaseElement.__to_string(e, level), self.children))

    @staticmethod
    def __padding_space(level):
        return ' ' * level * 2
