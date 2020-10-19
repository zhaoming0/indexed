#!/bin/sh
cd $(dirname $0)
git pull
git checkout .
for  n in `find keyword -name "*.xlsx"`
do
	echo $n
	now_time=$(date "+%Y-%m-%d %H:%M:%S")
	cp $n test.xlsx
	git add .
	git commit -am "Index  ${n#*/}   $now_time"
	git push origin master
done
