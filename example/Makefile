GEN=`which cfgen`

clean:
	rm -f output.conf

%.json:
	$(GEN) --parser json config.json $*

%.yaml:
	$(GEN) --parser yaml config.yaml $*
