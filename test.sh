#!/bin/bash

python3 make_commands.py config.json main main > commands.sh
docker run --mount type=bind,source=$(pwd),target=/home/dangswan/test aptest bash test/commands.sh
python3 make_commands.py config.json $1 $2 > commands.sh
docker run --mount type=bind,source=$(pwd),target=/home/dangswan/test aptest bash test/commands.sh
