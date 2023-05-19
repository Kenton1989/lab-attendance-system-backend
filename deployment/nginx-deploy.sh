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

#####################

echo installing Nginx...

apt-get update
apt-get install nginx

echo Nginx installed

echo status of Nginx
systemctl status nginx

#####################

echo changing firewall setting...

ufw allow 'Nginx HTTP'

echo firewall settings updated

#####################

bash ./deployment/set-nginx.conf.sh