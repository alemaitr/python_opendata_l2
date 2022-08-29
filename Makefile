SRC          := $(wildcard TD*.tex)
TARGETS  := $(patsubst %.tex,_build/%.pdf,$(SRC))

all: $(TARGETS)

_build/%.pdf: %.tex
	mkdir -p _build
	pdflatex --interaction=nonstopmode $^
	mv $(^:.tex=.pdf) _build/
	rm -f $(^:.tex=.out) $(^:.tex=.aux) $(^:.tex=.log)

clean:
	rm -f *.out *.aux *.log
