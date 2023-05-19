# if [[ $UID != 0 ]]; then
#     echo "Please run this script with sudo:"
#     echo "sudo $0 $*"
#     exit 1
# fi

#########################
MANAGE_PY=manage.py

echo checking location of script...

if [ ! -f "$MANAGE_PY" ]; then
    cd ..
fi

if [ ! -f "$MANAGE_PY" ]; then
    echo cannot find $MANAGE_PY, please make sure you are running this script in the Django project root folder
    exit 1
fi

#########################
echo
echo installing python...
sudo apt-get update
# python 3.8
sudo apt-get install python3.8 python3.8-dev python3.8-distutils python3.8-venv
echo
#########################

echo
echo creating python virtual environment...
python3.8 -m venv venv/
source venv/bin/activate
echo

#########################

echo
echo installing python packages...

# additional dependencies of mysqlclient
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
# install wheel as some package use it
pip install wheel
pip install -r requirements.txt

echo required python packages installed
echo

##########################

echo
bash ./deployment/mysql-deploy.sh
echo

##########################

echo
python3.8 ./deployment/gen-env-file.py
echo

##########################

echo
bash ./deployment/be-quick-deploy.sh &

exit $?