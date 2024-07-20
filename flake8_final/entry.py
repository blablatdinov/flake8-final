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
from collections.abc import Generator
from typing import final


@final
class ClassVisitor(ast.NodeVisitor):
    """Class visitor for checking final deorator."""

    def __init__(self) -> None:
        """Ctor."""
        self.problems: list[int] = []

    def visit_ClassDef(self, node) -> None:  # noqa: N802. Flake8 plugin API
        """Visit by classes."""
        from astpretty import pprint
        final_found = False
        for deco in node.decorator_list:
            # pprint(deco)
            print('deco = ', end='')
            pprint(deco)
            if isinstance(deco, ast.Call):
                # assert False
                final_found = final_found or deco.func.value.id == 'final'
            else:
                final_found = final_found or deco.id == 'final'
        if not final_found:
            self.problems.append(node.lineno)
        self.generic_visit(node)


@final
class Plugin:
    """Flake8 plugin."""

    def __init__(self, tree) -> None:
        """Ctor."""
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, type], None, None]:
        """Entry."""
        visitor = ClassVisitor()
        visitor.visit(self._tree)
        for line in visitor.problems:  # noqa: WPS526
            yield (line, 0, 'FIN100 class must be final', type(self))
