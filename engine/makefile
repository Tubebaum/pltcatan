# makefile

start: start.py
	python start.py

debug:
	# pdb.set_trace()
	python -m pdb start.py

.PHONY: clean
clean:
	find . -name "*.pyc" -exec rm -rf {} \;
