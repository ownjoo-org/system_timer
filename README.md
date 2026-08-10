# system_timer

[![License](https://img.shields.io/github/license/ownjoo/system_timer)](LICENSE)
[![Top language](https://img.shields.io/github/languages/top/ownjoo/system_timer)](https://github.com/ownjoo/system_timer) [![Stars](https://img.shields.io/github/stars/ownjoo/system_timer)](https://github.com/ownjoo/system_timer/stargazers) [![Forks](https://img.shields.io/github/forks/ownjoo/system_timer)](https://github.com/ownjoo/system_timer/forks) [![Issues](https://img.shields.io/github/issues/ownjoo/system_timer)](https://github.com/ownjoo/system_timer/issues) [![Pull requests](https://img.shields.io/github/issues-pr/ownjoo/system_timer)](https://github.com/ownjoo/system_timer/pulls)

A small, dependency-free `timeout` decorator that raises `TimeoutError` if a
function call runs longer than a given number of seconds, implemented via a
daemon thread (`Thread.join(timeout=...)`).

# SECURITY NOTE:
I wrote the .py files.  You have my word that they don't do anything nefarious.  Even so, I recommend that you perform
your own static analysis and supply chain testing before use.  Many libraries are imported that are not in my own control.

## Usage

```python
from main import timeout

@timeout(seconds=5)
def slow_call():
    ...

try:
    slow_call()
except TimeoutError as e:
    print(f'gave up waiting: {e}')
```

## How it works

The decorator runs the wrapped call on a daemon thread and waits up to `seconds`
for it to finish (`Thread.join(timeout=seconds)`). This works identically on
every platform and from any calling thread.

**Limitation:** Python cannot forcibly kill a running thread. If the call doesn't
finish in time, this raises `TimeoutError` and returns control to the caller
immediately, but the wrapped function keeps running to completion on its worker
thread in the background -- it's abandoned, not aborted. The thread is created
with `daemon=True` specifically so an abandoned call never blocks interpreter
shutdown. Use this to stop *waiting* on a slow call, not to terminate runaway or
CPU-bound work.

## History: the original version never worked

The original implementation used `signal.alarm` and looked plausible, but it
never actually enforced a timeout:

- `signal.signal(seconds, handler)` passed the timeout value itself where
  `signal.SIGALRM` belonged, so it silently hijacked whichever unrelated signal
  happened to share that number instead -- e.g. `seconds=2` collided with
  `SIGINT`, `seconds=9` would have raised `RuntimeError` (`SIGKILL` can't be
  caught), `seconds=10` would have hijacked `SIGUSR1`, and so on. `signal.alarm()`
  -- the call that actually schedules a delayed signal -- was never invoked at
  all, so no timer was ever set.
- The `finally` block unconditionally re-raised `TimeoutError` (by manually
  raising the hijacked signal) after the wrapped call returned, regardless of
  whether it had actually taken too long. A call with no `sleep()` at all still
  raised `TimeoutError`.
- It could never have run on Windows in the first place, since `signal.SIGALRM`
  doesn't exist there.

The one demo in this repo (`seconds=2`, `sleep(3)`) happened to produce output
indistinguishable from a correctly working timeout -- print, pause, `TimeoutError`
caught, done -- which is exactly why the bug went unnoticed: waiting for the full
call to finish and then always raising afterward looks identical to a real
2-second timeout when the only test case run is one where both explanations
predict the same result.

## See also

For a tested, packaged version of this decorator -- plus an async equivalent
built on `asyncio.timeout()` -- see
[`oj_toolkit.timing.timeout`](https://github.com/ownjoo/ownjoo-toolkit) and
[`oj_toolkit.asynchronous.async_timeout`](https://github.com/ownjoo/ownjoo-toolkit)
in [ownjoo-toolkit](https://github.com/ownjoo/ownjoo-toolkit).
