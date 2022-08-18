#!/bin/bash

PYTHON_PATH=$(which python3)
if [ "$PYTHON_PATH" == "python3 not found" ]
then
  echo "Python 3 not install in your computer. Please install it before running this script again"
  exit 0
fi
$PYTHON_PATH -m pip install -r requirements.txt

MAIN_SCRIPT="$(pwd)/main.py"
ZSH_SCRIPT="$PYTHON_PATH $MAIN_SCRIPT"
echo -e "#!/bin/zsh\n$ZSH_SCRIPT" > syncNotionCalendar.zsh

$PYTHON_PATH src/init_conf.py config.ini
$PYTHON_PATH src/init_cron.py
echo "Synchronisation of your databases ...."
./syncNotionCalendar.zsh
echo "Installation done"


