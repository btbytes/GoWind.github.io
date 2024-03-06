HTML=$(patsubst %.md, %.html, $(wildcard *.md))

%.html: %.md before Makefile
	pandoc -s --css basic.css -f markdown -B before -o $@ $<

index.md: index.txt genindex.py
	./genindex.py

all: $(HTML)


