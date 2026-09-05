.PHONY: install test lint api ui

install:
	python -m pip install -e '.[dev,api,ui]'

test:
	pytest

lint:
	ruff check src tests

api:
	uvicorn rehabdynamics.api.main:app --reload

ui:
	streamlit run src/rehabdynamics/ui/app.py
