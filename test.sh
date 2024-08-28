#!/bin/bash

docker run --mount type=bind,source=$(pwd),target=/home/dangswan/test aptest test/test.py test/config.json $1 $2
