#! bin/bash

default_dir=$(pwd)

apt install python3-pip

pip install virtualenv
python3 -m venv .

<<<<<<< HEAD
source bin/activate
pip install -r requirements.txt
=======
source talking-stick/bin/activate
pip install -r requirements.txt
cd $default_dir/talking-stick
>>>>>>> dev

mkdir logs
mkdir json
touch json/guilds.json
echo "{}" >> json/guilds.json
<<<<<<< HEAD
=======
mv $default_dir/src .
mv $default_dir/bot.py .
>>>>>>> dev

touch .env
read -p "Enter your bot token: " token
echo "TOKEN=\"$token\"" >> .env

<<<<<<< HEAD
deactivate

echo "Installation complete"
=======
rm install.sh
rm requirements.txt
deactivate

echo "Installation complete"
>>>>>>> dev
