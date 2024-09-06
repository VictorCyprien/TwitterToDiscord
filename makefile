install:
	python3 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt

run:
	. venv/bin/activate; python main.py	

clean:
	rm -R venv
	find -iname "*.pyc" -delete
