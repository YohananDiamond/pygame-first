# pygame-first

An evolution of my first pygame project.

It's more of an engine, a very simple one.

## Running

The current method of running the file is hella unstable.

First, try running the file via `python3 main.py`. `python3.7` is recommended.

If it doesn't work (probably because some class doesn't exist), run `make config` (to install `strip-hints`, a pip package which removes type annotations) and then `make run` (which uses strip-hints to remove type annotations on the fly and run it, without modifying the file).
