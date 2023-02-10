all: serve

.PHONY: serve
serve:
	uvicorn main:app --reload

.PHONY: install
install:
	pip install --upgrade pip
	pip install -r requirements.txt
	

