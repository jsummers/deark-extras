#!/bin/bash

function getcrc () {
	actualcrc=$(deark -m crc "$srcfn" | grep CRC-32-IEEE | cut -dx -f2)
}

for srcfn in *.bin
do
	expectedcrc=${srcfn/*_/}
	expectedcrc=${expectedcrc/%.bin}
	getcrc
	if [ "$actualcrc" = "$expectedcrc" ]
	then
		echo "ok    $srcfn"
	else
		echo "ERROR $srcfn"
	fi
done

