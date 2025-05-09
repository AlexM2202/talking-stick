#! bin/bash

script_dir=$(dirname "$(readlink -f "$0")")

cd $script_dir
<<<<<<< HEAD
source bin/activate
python3 bot.py
=======
source talking-stick/bin/activate
python3 bot.py
>>>>>>> dev
