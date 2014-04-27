all: navigator_ui.py

navigator_ui.py : navigator.ui
	pyuic4 $< > $@
