all: en

de:
	./src/build_model.sh lang/de tmp/lang/de

en:
	./src/build_model.sh lang/en tmp/lang/en

install: tools/sequitur-g2p tools/ascii-ipa

tools/sequitur-g2p:
	git clone https://github.com/sequitur-g2p/sequitur-g2p.git tools/sequitur-g2p
	cd tools/sequitur-g2p && make
	cd tools/sequitur-g2p && python setup.py install --prefix `pwd`

tools/ascii-ipa:
	git clone https://github.com/coruus/ascii-ipa.git tools/ascii-ipa
	echo '' > tools/ascii-ipa/__init__.py

clean:
	rm -rf tools/sequitur-g2p
	rm -rf tools/ascii-ipa

