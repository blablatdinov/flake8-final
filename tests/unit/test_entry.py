# The MIT License (MIT)
#
# Copyright (c) 2023 blablatdinov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import ast

import pytest

from flake8_final.entry import Plugin


@pytest.fixture
def plugin_run():
    """Fixture for easy run plugin."""
    def _plugin_run(code: str) -> list[tuple[int, int, str]]:  # noqa: WPS430
        """Plugin run result."""
        plugin = Plugin(ast.parse(code))
        res = []
        for viol in plugin.run():
            res.append((
                viol[0],
                viol[1],
                viol[2],
            ))
        return res
    return _plugin_run


def test_wrong(plugin_run):
    """Test wrong case."""
    got = plugin_run('\n'.join([
        'class Animal(object):',
        '',
        '    def move(self, to_x: int, to_y: int):',
        '        # Some logic for change coordinates',
        '        pass',
        '',
        '    def sound(self):',
        '        print("Abstract animal sound")',
        '',
    ]))

    assert got == [
        (
            1,
            0,
            'FIN100 class must be final',
        ),
    ]


def test_valid(plugin_run):
    """Test valid case."""
    got = plugin_run('\n'.join([
        '@final',
        'class Animal(object):',
        '',
        '    def move(self, to_x: int, to_y: int):',
        '        # Some logic for change coordinates',
        '        pass',
        '',
        '    def sound(self):',
        '        print("Abstract animal sound")',
        '',
    ]))

    assert not got


def test_two_deco(plugin_run):
    """Test two decorator case."""
    got = plugin_run('\n'.join([
        '@final',
        '@attrs.define(frozen=True)',
        'class Animal(object):',
        '',
        '    def move(self, to_x: int, to_y: int):',
        '        # Some logic for change coordinates',
        '        pass',
        '',
        '    def sound(self):',
        '        print("Abstract animal sound")',
        '',
    ]))

    assert not got


def test_typing_final(plugin_run):
    """Test absolute path."""
    got = plugin_run('\n'.join([
        '@typing.final',
        'class Animal(object):',
        '',
        '    def move(self, to_x: int, to_y: int):',
        '        # Some logic for change coordinates',
        '        pass',
        '',
        '    def sound(self):',
        '        print("Abstract animal sound")',
        '',
    ]))

    assert not got


@pytest.mark.parametrize('base_class', [
    'Protocol',
    'typing.Protocol',
    't.Protocol',
    't.Protocol, OtherClass',
    'OtherClass, Protocol',
    'OtherClass, t.Protocol',
    'Protocol[Mammal]',
])
def test_protocols(plugin_run, base_class):
    """Test protocols."""
    got = plugin_run('\n'.join([
        'class Animal({0}):'.format(base_class),
        '',
        '    def move(self, to_x: int, to_y: int):',
        '        # Some logic for change coordinates',
        '        pass',
        '',
        '    def sound(self):',
        '        print("Abstract animal sound")',
        '',
    ]))

    assert not got


def test_generic_base(plugin_run):
    got = plugin_run('\n'.join([
        '@final',
        'class Dog(Animal[Mammal]):',
        '',
        '    def move(self, to_x: int, to_y: int):',
        '        # Some logic for change coordinates',
        '        pass',
        '',
        '    def sound(self):',
        '        print("Abstract animal sound")',
        '',
    ]))

    assert not got