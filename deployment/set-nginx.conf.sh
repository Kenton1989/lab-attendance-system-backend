if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

# Absolute path to this script
SCRIPT=$(readlink -f "$0")
# Absolute path of the dir this script is in
SCRIPT_DIR_PATH=$(dirname "$SCRIPT")

NGINX_CONF_TEMPLATE=$SCRIPT_DIR_PATH/nginx.conf.template
TEMP_CONF=/tmp/tmp.nginx.conf
NGINX_CONF_PATH=/etc/nginx/nginx.conf

echo creating nginx.conf using template $NGINX_CONF_TEMPLATE...
bash $SCRIPT_DIR_PATH/make-nginx.conf.sh <$NGINX_CONF_TEMPLATE >$TEMP_CONF

echo copying $TEMP_CONF to $NGINX_CONF_PATH...
cp $TEMP_CONF $NGINX_CONF_PATH

echo reload nginx...

nginx -s reload