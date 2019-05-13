ACTIVATE = source venv/bin/activate &&


all: start

venv: requirements.txt
	python3 -m venv venv
	$(ACTIVATE) pip3 install -r requirements.txt

start: venv
	$(ACTIVATE) python3 ./ketomojo/process_ketomojo.py -o files/keto_mojo_readings.csv

.PHONY: start all