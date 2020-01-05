run: config typecheck
	strip-hints ./main.py | python3

typecheck:
	mypy main.py

config:
	if ! pip3 show strip-hints >/dev/null 2>/dev/null; then pip3 install strip-hints; fi
	if ! pip3 show mypy >/dev/null 2>/dev/null; then pip3 install mypy; fi
