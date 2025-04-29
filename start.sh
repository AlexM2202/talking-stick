#! bin/bash

script_dir=$(dirname "$(readlink -f "$0")")

cd $script_dir
source talking-stick/bin/activate
python3 bot.py