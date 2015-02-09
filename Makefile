# makefile automate
PY := $(VENV)bin/python
PIP := $(VENV)bin/pip
VENV := ~/.virtualenvs/pyr2-env/
PASTER := $(VENV)bin/pserve
GUNICORN := $(VENV)bin/gunicorn
CELERY := $(VENV)bin/celery

KENSAKU_INI = gunicorn.ini

.PHONY: run_app
run_app:
	$(GUNICORN) --pid-file=app.pid --paster $(KENSAKU_INI) &
.PHONY: run_celery
run_celery:
	$(CELERY) worker -A pyramid_celery.celery_app --ini $(KENSAKU_INI) -B --pidfile celeryd.pid &
.PHONY: run
run: run_celery run_app

.PHONY: stop
stop: stop_app stop_celery
.PHONY: stop_celery
stop_celery:
	pkill celery
	rm celeryd.pid || true
.PHONY: stop_app
stop_app:
	pkill gunicorn
	rm app.pid || true