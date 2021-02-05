
test:
	# pip install pyinstaller
	pyinstaller --onefile while-ss.py
	mv dist/while-ss .
	rm while-ss.spec
	rm -r __pycache__ build dist

all:
	python3 while-ss.py

clean: 
	rm while-ss