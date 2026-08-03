# system_timer

[![License](https://img.shields.io/github/license/ownjoo/system_timer)](LICENSE)
[![Top language](https://img.shields.io/github/languages/top/ownjoo/system_timer)](https://github.com/ownjoo/system_timer) [![Stars](https://img.shields.io/github/stars/ownjoo/system_timer)](https://github.com/ownjoo/system_timer/stargazers) [![Forks](https://img.shields.io/github/forks/ownjoo/system_timer)](https://github.com/ownjoo/system_timer/forks) [![Issues](https://img.shields.io/github/issues/ownjoo/system_timer)](https://github.com/ownjoo/system_timer/issues) [![Pull requests](https://img.shields.io/github/issues-pr/ownjoo/system_timer)](https://github.com/ownjoo/system_timer/pulls)
A Python decorator (`@timeout(seconds=...)`) that raises `TimeoutError` if the decorated
function doesn't return within the given number of seconds, implemented via
`signal.alarm`.

# SECURITY NOTE:
I wrote the .py files.  You have my word that they don't do anything nefarious.  Even so, I recommend that you perform
your own static analysis and supply chain testing before use.  Many libraries are imported that are not in my own control.

# usage
```python
from main import timeout

@timeout(seconds=5)
def slow_call():
    ...
```
