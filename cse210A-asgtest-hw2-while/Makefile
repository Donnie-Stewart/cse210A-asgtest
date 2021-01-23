
all:
	pip install pyinstaller
	pyinstaller --onefile while.py
	mv dist/while .
	rm while.spec
	rm -r __pycache__ build dist

test:
	python3 while.py