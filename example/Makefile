GEN=`which cfgen`

clean:
	rm -f output.conf

%.json:
	$(GEN) -t `pwd` -o `pwd` -p json config.json $*

%.yaml:
	$(GEN) -t `pwd` -o `pwd` -p yaml config.yaml $*
