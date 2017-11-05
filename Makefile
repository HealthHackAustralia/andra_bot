serve:
	FLASK_APP=app.py flask run --port 8080 --host localhost
.PHONY: serve

test:
	python robot.py
