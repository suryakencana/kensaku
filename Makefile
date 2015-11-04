# makefile automate
PY := $(VENV)bin/python
PIP := $(VENV)bin/pip
VENV := venv/
PASTER := $(VENV)bin/pserve
GUNICORN := $(VENV)bin/gunicorn
CELERY := $(VENV)bin/celery

KENSAKU_INI = gunicorn.ini

.PHONY: run_app
run_app:
	$(GUNICORN) --paster $(KENSAKU_INI) --reload &
.PHONY: run_celery
run_celery:
	$(CELERY) worker -A pyramid_celery.celery_app --ini $(KENSAKU_INI) -B &
.PHONY: run
run: run_celery run_app

.PHONY: stop
stop: stop_app stop_celery
.PHONY: stop_celery
stop_celery:
	pkill celery
.PHONY: stop_app
stop_app:
	pkill gunicorn
