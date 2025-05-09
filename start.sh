#! bin/bash

script_dir=$(dirname "$(readlink -f "$0")")

cd $script_dir
source bin/activate
python3 bot.py
