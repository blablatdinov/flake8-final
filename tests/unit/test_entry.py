# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

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
    """Test generic base class."""
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
