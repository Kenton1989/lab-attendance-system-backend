if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

MANAGE_PY=manage.py

if [ ! -f "$MANAGE_PY" ]; then
    cd ..
fi

if [ ! -f "$MANAGE_PY" ]; then
    echo cannot find $MANAGE_PY, please make sure you are running this script in the Django project root folder
    exit 1
fi

#############################

echo installing node.js...

curl -sL https://deb.nodesource.com/setup_16.x -o /tmp/nodesource_setup.sh
bash /tmp/nodesource_setup.sh
apt-get install nodejs
echo installed node.js $(node --version)

###########################

bash ./deployment/fe-quick-deploy.sh