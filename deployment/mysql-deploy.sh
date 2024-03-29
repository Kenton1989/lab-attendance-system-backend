set -e # exit when error happens on any line
set -o pipefail # return error code of last executed command

#########################

# if [[ $UID != 0 ]]; then
#     echo "Please run this script with sudo:"
#     echo "sudo $0 $*"
#     exit 1
# fi

# ########################

# Absolute path to this script
SCRIPT=$(readlink -f "$0")
# Absolute path of the dir this script is in
SCRIPT_DIR_PATH=$(dirname "$SCRIPT")

INIT_SQL_SCRIPT=$SCRIPT_DIR_PATH/init-database.sql

########################

echo installing MySQL...

sudo apt-get update
sudo apt-get install mysql-server || exit 1

echo installed MySQL

########################

echo starting MySQL service

sudo systemctl start mysql || exit 1

echo started MySQL service

########################

echo 
echo Please ensure you have updated the password in init-database.sql.
echo Did you updated that password? "[y/n]"
echo '(If you are not sure what I am saying, please answer "n" and read README.md first)'
read ANSWER || exit
if [[ "$ANSWER" != "y" && "$ANSWER" != "Y" ]]; then
    echo Please update the password and then run the script again.
    exit 1
fi

sudo mysql < "$INIT_SQL_SCRIPT" || exit 1