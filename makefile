NOPYTHON = false
PYTHON = python
ifeq ($(shell which python3),)
	python_version_full := $(wordlist 2,4,$(subst ., ,$(shell python --version 2>&1)))
	python_version_major := $(word 1,${python_version_full})
	NOPYTHON = true
	ifeq ( $(python_version_major), 3 )
		NOPYTHON = false
		PYTHON = python
		PYTHON-PIP = pip
	endif
else
	PYTHON = python3
	PYTHON-PIP = pip3
endif

.PHONY : all
.DEFAULT: help

help:
	@echo "make prepare"
	@echo "    prepare development environment, use only once"
	@echo "make install"
	@echo "    install all python requirements, use only once"
	@echo "make start"
	@echo "    start the simulation as in init.py"
	@echo "make start-fast"
	@echo "    start a fast simulation (results will be less accurate)"
	@echo "make start-normal"
	@echo "    start a default simulation (results can be considerate good)"
	@echo "make start-slow"
	@echo "    this is the best simulation (but it is really slow)"
	@echo "make start-verbose"
	@echo "    start the simulation with verbose flag"
	@echo "make start-debug"
	@echo "    start the simulation using a default test"
	@echo "make start-beautiful"
	@echo "    start the simulation in the browser with a user interface"
	@echo "make start-beautiful-debug"
	@echo "    start the simulation in the browser with a user interface and a default test"
	@echo "make model"
	@echo "    start the model"
	@echo "make analysis"
	@echo "    start the analysis of data"
	@echo "make start-all-in-one"
	@echo "    start a fast simulation then the model and at the end the analysis of data"

prepare:
	sudo apt-get install python3
	sudo apt-get install python3-tk
	sudo apt-get install python3-pip

check_version:
	@if [ ${NOPYTHON} = false ]; \
		then ${PYTHON} --version; \
		else \
			echo "Sorry :( THIS PROJECT NEEDS PYTHON3!"; \
			echo "Your current version: "; \
			${PYTHON} --version; \
			echo "> Running 'make prepare' to install python3, python3-tk and python3-pip for you!"; \
			make prepare; \
			make install; \
			echo "> Trying again . . ."; \
	fi

install: check_version
	${PYTHON-PIP} install -r requirements.txt

start: check_version
	${PYTHON} -W ignore simulator -nodb

start-fast: check_version
	${PYTHON} -W ignore simulator -dt 1000 -r 5 -nodb

start-normal: check_version
	${PYTHON} -W ignore simulator -dt 1000 -r 10 -nodb

start-slow: check_version
	${PYTHON} -W ignore simulator -dt 1500 -r 50 -nodb

start-verbose: check_version
	${PYTHON} -W ignore simulator -vb

start-debug: check_version
	${PYTHON} -W ignore simulator -db

start-beautiful: check_version
	${PYTHON} -W ignore ./simulator/main_interface.py -nodb

start-beautiful-debug: check_version
	${PYTHON} -W ignore ./simulator/main_interface.py -db

analysis: check_version
	${PYTHON} -W ignore analysis

model: check_version
	${PYTHON} -W ignore model

start-all-in-one: check_version start-normal model analysis
	@echo "done"
