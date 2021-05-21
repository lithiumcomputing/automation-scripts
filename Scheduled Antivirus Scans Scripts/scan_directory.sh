# Author: Jim Li
# Date: 24 November 2016
#
# A simple script to scan a user-specified directory using ClamAV.

#!/bin/bash

echo Please enter the directory to scan:
DIR=""
read DIR

fileName="scan_results.txt"
tilde="~"

# Handle the case where the user decides to start the directory path with a tilde (~).
# It seems that bash does not recognize the tilda when executing independant scripts.
if [ $(echo $DIR | head -c 1) == $tilde ]
then
	echo Scanning the Directory: $(echo $(echo ~)${DIR:1})
	clamscan -r -i --verbose $(echo $(echo ~)${DIR:1}) > $fileName
else
	echo Scanning the Directory: $DIR
	clamscan -r -i --verbose $DIR > $fileName
fi

