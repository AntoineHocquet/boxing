.PHONY: all lint format test typecheck coverage debug pudb fire clean

PYTHON := PYTHONPATH=. python

all: lint typecheck test coverage

lint:
	@echo "🔍 Running ruff (lint)..."
	$(PYTHON) -m ruff check src/

format:
	@echo "🧹 Formatting with black and ruff..."
	$(PYTHON) -m black src/
	$(PYTHON) -m ruff format src/

typecheck:
	@echo "🔎 Running mypy..."
	$(PYTHON) -m mypy src/

test:
	@echo "🧪 Running pytest..."
	$(PYTHON) -m pytest -vv -s

coverage:
	@echo "📊 Running coverage..."
	$(PYTHON) -m coverage run -m pytest
	$(PYTHON) -m coverage report
	$(PYTHON) -m coverage html

debug:
	@echo "🐞 Debugging tests with pudb..."
	$(PYTHON) -m pytest --pdbcls=pudb.debugger:Debugger

pudb:
	@echo "🔎 pudb main boxing entrypoint..."
	$(PYTHON) -m pudb boxing.py

fire:
	@echo "🔥 Running python-fire CLI..."
	$(PYTHON) src/cli.py $(ARGS)

# Use like:
# make fire ARGS="train --epochs=10"
# make fire ARGS="fight --model_a=models/A.pt --model_b=models/B.pt"

clean:
	@echo "🧼 Cleaning cache..."
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf .pytest_cache .mypy_cache htmlcov


# for training
train:
	$(PYTHON) boxing.py train

retrain:
	$(PYTHON) boxing.py retrain

animate:
	$(PYTHON) boxing.py animate --log 100
