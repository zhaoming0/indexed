#!/bin/bash
cd $(dirname $0)
now_time=$(date "+%Y-%m-%d %H:%M:%S")
git add test.xlsx
git commit -am "manual test for index $now_time"
git push origin main
