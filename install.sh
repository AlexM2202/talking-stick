#! bin/bash

default_dir=$(pwd)

apt install python3-pip

pip install virtualenv
python3 -m venv .

source bin/activate
pip install -r requirements.txt

mkdir logs
mkdir json
touch json/guilds.json
echo "{}" >> json/guilds.json

touch .env
read -p "Enter your bot token: " token
echo "TOKEN=\"$token\"" >> .env

deactivate

echo "Installation complete"
