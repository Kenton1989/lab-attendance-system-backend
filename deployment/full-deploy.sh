if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

MANAGE_PY=manage.py

echo checking location of script...

if [ ! -f "$MANAGE_PY" ]; then
    cd ..
fi

if [ ! -f "$MANAGE_PY" ]; then
    echo cannot find $MANAGE_PY, please make sure you are running this script in the Django project root folder
    exit 1
fi

apt-get update

bash ./deployment/be-full-deploy.sh
bash ./deployment/fe-full-deploy.sh

bash ./deployment/set-nginx.conf.sh