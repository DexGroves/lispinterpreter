test:
		pip install -e .; pytest .

install:
		pip install -e .

lint:
		mypy src/