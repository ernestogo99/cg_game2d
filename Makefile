.PHONY: run
run:
	python3 main.py

.PHONY: clean
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type f -name '.DS_Store' -delete
