<!---
The MIT License (MIT)

Copyright (c) 2023 blablatdinov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
--->

# flake8-final

[![test](https://github.com/blablatdinov/flake8-final/actions/workflows/test.yml/badge.svg)](https://github.com/blablatdinov/flake8-final/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/blablatdinov/flake8-final/branch/master/graph/badge.svg)](https://codecov.io/gh/blablatdinov/flake8-final)
[![Python Version](https://img.shields.io/pypi/pyversions/flake8-final.svg)](https://pypi.org/project/flake8-final/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

## Background

Implementation inheritance can lead to brittle and hard-to-maintain code. By enforcing the use of the `@final` decorator, this plugin aims to encourage composition over inheritance, promoting better software design principles.

[yegor256 blog post](https://www.yegor256.com/2016/09/13/inheritance-is-procedural.html)

## Installation

To install `flake8-final`, you can use `pip`:

```bash
pip install flake8-final
```

## Usage

After installing the plugin, flake8 will automatically use it when you run the following command:

bash

flake8 your_project_directory

The plugin will check each class definition to ensure it has a @final decorator. If a class is missing the @final decorator, an error will be reported.

## Example

Given the following Python code:

```python
class MyClass:
    pass
```

Running flake8 will produce the following error:

```
your_file.py:1:1: FIN100 class must be final
```

Adding the `@final` decorator will resolve the error:

```python
from typing import final

@final
class MyClass:
    pass
```

## License

[MIT](https://github.com/blablatdinov/flake8-final/blob/master/LICENSE)


## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [9899cb192f754a566da703614227e6d63227b933](https://github.com/wemake-services/wemake-python-package/tree/9899cb192f754a566da703614227e6d63227b933). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/9899cb192f754a566da703614227e6d63227b933...master) since then.
