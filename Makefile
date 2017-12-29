.PHONY: deps play play-gui

deps:
	python3.6 -m pip install --upgrade -r requirements.txt

play:
	./play.py

play-gui:
	./play.py --gui