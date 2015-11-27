all: en de fr nl

en:
	./src/build_model.sh lang/en tmp/lang/en

de:
	./src/build_model.sh lang/de tmp/lang/de

fr:
	./src/build_model.sh lang/fr tmp/lang/fr

nl:
	./src/build_model.sh lang/nl tmp/lang/nl


install: tools/sequitur-g2p

tools/sequitur-g2p:
	git clone https://github.com/sequitur-g2p/sequitur-g2p.git tools/sequitur-g2p
	cd tools/sequitur-g2p && make
	cd tools/sequitur-g2p && python setup.py install --prefix `pwd`

clean:
	rm -rf tools/sequitur-g2p

