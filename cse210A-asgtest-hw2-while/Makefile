all:
	python3 while.py

test:
	pip install pyinstaller
	pyinstaller --onefile arith.py
	mv dist/arith .
	rm arith.spec
	rm -r __pycache__ build dist