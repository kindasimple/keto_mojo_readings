ACTIVATE = source venv/bin/activate &&


all: start

venv:
	virtualenv venv
	$(ACTIVATE) pip3 install -r requirements.txt

start: venv
	$(ACTIVATE) python3 ./process_ketomojo.py -o keto_mojo_readings.csv

.PHONY: start all